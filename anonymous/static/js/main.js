function show_more(id) {
    var showMore = document.getElementById("showMore"+id);
    var showLess = document.getElementById("showLess"+id);
    var more = document.getElementById("more"+id);
  
    if (showMore.style.display === "none") {
      showMore.style.display = "inline";
      more.style.display = "none";
      showLess.style.display = "none"
    } else {
      showMore.style.display = "none";
      more.style.display = "inline";
      showLess.style.display = "inline"
    }
  }