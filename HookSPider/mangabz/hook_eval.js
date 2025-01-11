// 脚本来源：微信群里收藏的，忘记是哪个大佬发的了，如有侵权联系我删除哈
window.__cr_eval = window.eval;
var myeval = function(src) {
    console.log('eval:', src);
    return window.__cr_eval(src)
};
var _myeval = myeval.bind(null);
_myeval.toString = window.__cr_eval.toString;
Object.defineProperty(window, 'eval', { value: _myeval });