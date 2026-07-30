window.MathJax = {
  loader: {
    load: ["[tex]/boldsymbol"]
  },
  tex: {
    inlineMath: [["\\(", "\\)"], ["$", "$"]],
    displayMath: [["\\[", "\\]"], ["$$", "$$"]],
    processEscapes: true,
    processEnvironments: true,
    packages: { "[+]": ["boldsymbol"] }
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  },
  svg: {
    fontCache: "global"
  }
};

document$.subscribe(() => {
  if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
    MathJax.typesetClear()
    MathJax.typesetPromise()
  }
})
