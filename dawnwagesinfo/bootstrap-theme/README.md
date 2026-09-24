# Bootstrap theme

The site loads Bootstrap from committed static files; nothing is built when
developing or deploying:

- `static/vendor/bootstrap/bootstrap.theme.min.css`: Bootstrap 5.3.8 compiled
  with the variables in `bootstrap-theme.scss` (breakpoints, colors, fonts,
  spacing, component styles).
- `static/vendor/bootstrap/bootstrap.bundle.min.js`: stock Bootstrap 5.3.8 JS.

Site-specific styles live in `static/css/site.css` (plain CSS, edit directly).

## Changing a Bootstrap variable

Only needed when you edit `bootstrap-theme.scss`. Uses the standalone Dart Sass
binary; no Node or npm.

```bash
brew install sass/sass/sass
curl -L https://github.com/twbs/bootstrap/archive/refs/tags/v5.3.8.tar.gz | tar -xz -C /tmp
mkdir -p /tmp/bs-src/bootstrap && cp -R /tmp/bootstrap-5.3.8/scss /tmp/bs-src/bootstrap/
sass --no-source-map --style=compressed --quiet-deps \
  --load-path=/tmp/bs-src \
  dawnwagesinfo/bootstrap-theme/bootstrap-theme.scss \
  dawnwagesinfo/static/vendor/bootstrap/bootstrap.theme.min.css
```

Commit the regenerated CSS.
