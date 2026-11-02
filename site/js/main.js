(function () {
  var btn = document.querySelector(".menu-btn");
  var list = document.getElementById("nav-list");
  if (btn && list) {
    btn.addEventListener("click", function () {
      var open = list.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    list.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        list.classList.remove("open");
        btn.setAttribute("aria-expanded", "false");
        btn.setAttribute("aria-label", "Open menu");
      });
    });
  }

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("in"); });
  }

  var chips = document.querySelectorAll(".chip[data-filter]");
  chips.forEach(function (c) {
    c.addEventListener("click", function () {
      chips.forEach(function (x) { x.setAttribute("aria-pressed", x === c ? "true" : "false"); });
      var f = c.dataset.filter;
      document.querySelectorAll(".post[data-cat]").forEach(function (p) {
        p.hidden = !(f === "all" || p.dataset.cat === f);
      });
    });
  });

  var search = document.getElementById("glossary-search");
  if (search) {
    search.addEventListener("input", function () {
      var q = search.value.trim().toLowerCase();
      var n = 0;
      document.querySelectorAll(".term").forEach(function (t) {
        var match = t.textContent.toLowerCase().indexOf(q) > -1;
        t.hidden = !match;
        if (match) n++;
      });
      document.getElementById("glossary-empty").hidden = n > 0;
    });
  }

  var form = document.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll("[required]").forEach(function (field) {
        var err = field.parentElement.querySelector(".err");
        var bad = !field.value.trim() || (field.type === "email" && !/^\S+@\S+\.\S+$/.test(field.value));
        if (err) err.textContent = bad ? (field.type === "email" ? "Enter an email address." : "This field is required.") : "";
        field.setAttribute("aria-invalid", bad ? "true" : "false");
        if (bad) ok = false;
      });
      if (!ok) return;
      var v = function (id) {
        var el = document.getElementById(id);
        return el ? el.value.trim() : "";
      };
      form.hidden = true;
      var done = document.getElementById("form-ok");
      done.hidden = false;
      done.focus();
    });
  }
})();
