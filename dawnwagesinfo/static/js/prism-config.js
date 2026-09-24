/* Point Prism's autoloader at the CDN copy of its language components. */
if (window.Prism && Prism.plugins.autoloader) {
  Prism.plugins.autoloader.languages_path = "https://cdn.jsdelivr.net/npm/prismjs@1.30.0/components/";
}
