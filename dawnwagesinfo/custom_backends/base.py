import os
import re
import threading
import time

import boto3
from django.db.backends.postgresql import base
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

# Aurora/RDS hostnames embed the region, e.g. db.cluster-abc.us-east-2.rds.amazonaws.com
RDS_HOST_REGION = re.compile(r"\.([a-z]{2}(?:-gov)?-[a-z]+-\d+)\.rds\.amazonaws\.com$")


class DatabaseWrapper(base.DatabaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._token = None
        self._token_expiry = 0
        self._token_lock = threading.Lock()
    
    def _region(self):
        """The cluster's AWS region: configured, or read from the RDS hostname.

        The IAM token must be signed for the cluster's own region, so don't guess.
        """
        region = getattr(settings, 'AWS_DEFAULT_REGION', None) or os.environ.get('AWS_REGION')
        if region:
            return region
        match = RDS_HOST_REGION.search(self.settings_dict['HOST'] or '')
        if match:
            return match.group(1)
        raise ImproperlyConfigured(
            "Set AWS_DEFAULT_REGION to the database's region; it couldn't be read from HOST."
        )

    def _generate_iam_token(self):
        """Generate a fresh IAM authentication token"""
        region = self._region()
        try:
            rds_client = boto3.client('rds', region_name=region)
            
            token = rds_client.generate_db_auth_token(
                DBHostname=self.settings_dict['HOST'],
                Port=self.settings_dict['PORT'],
                DBUsername=self.settings_dict['USER'],
                Region=region
            )
            return token
        except Exception as e:
            raise ImproperlyConfigured(f"Failed to generate IAM token: {e}")
    
    def _get_fresh_token(self):
        """Get a fresh token, using cache if still valid"""
        with self._token_lock:
            current_time = time.time()
            if not self._token or current_time >= (self._token_expiry - 60):
                self._token = self._generate_iam_token()
                self._token_expiry = current_time + (14 * 60)
            return self._token
    
    def get_connection_params(self):
        """Override to inject IAM token as password"""
        params = super().get_connection_params()
        params['password'] = self._get_fresh_token()
        params['sslmode'] = 'require'
        return params