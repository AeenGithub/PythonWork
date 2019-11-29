() => {
    function aa() {
        var spanDoms = document.querySelectorAll("span"), domLen = spanDoms.length;
        for (var i = 0; i < domLen; i++) {
            var v = spanDoms[i]
            if (v.textContent === "加载中") {
                return v.textContent
            }
        }
    }; return aa()
}