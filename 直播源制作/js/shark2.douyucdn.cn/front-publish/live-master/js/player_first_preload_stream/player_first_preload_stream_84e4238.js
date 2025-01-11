var hookt
!function(e) {
    var t = {};
    function __webpack_require__(r) {
        if (t[r])
            return t[r].exports;
        var n = t[r] = {
            i: r,
            l: !1,
            exports: {}
        };
        return e[r].call(n.exports, n, n.exports, __webpack_require__),
        n.l = !0,
        n.exports
    }
    hookt = __webpack_require__,
    __webpack_require__.m = e,
    __webpack_require__.c = t,
    __webpack_require__.d = function(e, t, r) {
        __webpack_require__.o(e, t) || Object.defineProperty(e, t, {
            enumerable: !0,
            get: r
        })
    }
    ,
    __webpack_require__.r = function(e) {
        "undefined" !== typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {
            value: "Module"
        }),
        Object.defineProperty(e, "__esModule", {
            value: !0
        })
    }
    ,
    __webpack_require__.t = function(e, t) {
        if (1 & t && (e = __webpack_require__(e)),
        8 & t)
            return e;
        if (4 & t && "object" === typeof e && e && e.__esModule)
            return e;
        var r = Object.create(null);
        if (__webpack_require__.r(r),
        Object.defineProperty(r, "default", {
            enumerable: !0,
            value: e
        }),
        2 & t && "string" != typeof e)
            for (var n in e)
                __webpack_require__.d(r, n, function(t) {
                    return e[t]
                }
                .bind(null, n));
        return r
    }
    ,
    __webpack_require__.n = function(e) {
        var t = e && e.__esModule ? function getDefault() {
            return e.default
        }
        : function getModuleExports() {
            return e
        }
        ;
        return __webpack_require__.d(t, "a", t),
        t
    }
    ,
    __webpack_require__.o = function(e, t) {
        return Object.prototype.hasOwnProperty.call(e, t)
    }
    ,
    __webpack_require__.p = "https://shark2.douyucdn.cn/front-publish/live-master/",
    __webpack_require__(__webpack_require__.s = "4a2a5")
}({
    "4a2a5": function(e, t, r) {
        "use strict";
        r.r(t);
        var i = i || function(e, t) {
            var r = {}
              , n = r.lib = {}
              , i = function n() {}
              , o = n.Base = {
                extend: function extend(e) {
                    i.prototype = this;
                    var t = new i;
                    return e && t.mixIn(e),
                    t.hasOwnProperty("init") || (t.init = function() {
                        t.$super.init.apply(this, arguments)
                    }
                    ),
                    t.init.prototype = t,
                    t.$super = this,
                    t
                },
                create: function create() {
                    var e = this.extend();
                    return e.init.apply(e, arguments),
                    e
                },
                init: function init() {},
                mixIn: function mixIn(e) {
                    for (var t in e)
                        e.hasOwnProperty(t) && (this[t] = e[t]);
                    e.hasOwnProperty("toString") && (this.toString = e.toString)
                },
                clone: function clone() {
                    return this.init.prototype.extend(this)
                }
            }
              , a = n.WordArray = o.extend({
                init: function init(e, t) {
                    e = this.words = e || [],
                    this.sigBytes = void 0 != t ? t : 4 * e.length
                },
                toString: function toString(e) {
                    return (e || c).stringify(this)
                },
                concat: function concat(e) {
                    var t = this.words
                      , r = e.words
                      , n = this.sigBytes;
                    if (e = e.sigBytes,
                    this.clamp(),
                    n % 4)
                        for (var i = 0; i < e; i++)
                            t[n + i >>> 2] |= (r[i >>> 2] >>> 24 - i % 4 * 8 & 255) << 24 - (n + i) % 4 * 8;
                    else if (65535 < r.length)
                        for (i = 0; i < e; i += 4)
                            t[n + i >>> 2] = r[i >>> 2];
                    else
                        t.push.apply(t, r);
                    return this.sigBytes += e,
                    this
                },
                clamp: function clamp() {
                    var t = this.words
                      , r = this.sigBytes;
                    t[r >>> 2] &= 4294967295 << 32 - r % 4 * 8,
                    t.length = e.ceil(r / 4)
                },
                clone: function clone() {
                    var e = o.clone.call(this);
                    return e.words = this.words.slice(0),
                    e
                },
                random: function random(t) {
                    for (var r = [], n = 0; n < t; n += 4)
                        r.push(4294967296 * e.random() | 0);
                    return new a.init(r,t)
                }
            })
              , s = r.enc = {}
              , c = s.Hex = {
                stringify: function stringify(e) {
                    var t = e.words;
                    e = e.sigBytes;
                    for (var r = [], n = 0; n < e; n++) {
                        var i = t[n >>> 2] >>> 24 - n % 4 * 8 & 255;
                        r.push((i >>> 4).toString(16)),
                        r.push((15 & i).toString(16))
                    }
                    return r.join("")
                },
                parse: function parse(e) {
                    for (var t = e.length, r = [], n = 0; n < t; n += 2)
                        r[n >>> 3] |= parseInt(e.substr(n, 2), 16) << 24 - n % 8 * 4;
                    return new a.init(r,t / 2)
                }
            }
              , u = s.Latin1 = {
                stringify: function stringify(e) {
                    var t = e.words;
                    e = e.sigBytes;
                    for (var r = [], n = 0; n < e; n++)
                        r.push(String.fromCharCode(t[n >>> 2] >>> 24 - n % 4 * 8 & 255));
                    return r.join("")
                },
                parse: function parse(e) {
                    for (var t = e.length, r = [], n = 0; n < t; n++)
                        r[n >>> 2] |= (255 & e.charCodeAt(n)) << 24 - n % 4 * 8;
                    return new a.init(r,t)
                }
            }
              , _ = s.Utf8 = {
                stringify: function stringify(e) {
                    try {
                        return decodeURIComponent(escape(u.stringify(e)))
                    } catch (e) {
                        throw Error("Malformed UTF-8 data")
                    }
                },
                parse: function parse(e) {
                    return u.parse(unescape(encodeURIComponent(e)))
                }
            }
              , f = n.BufferedBlockAlgorithm = o.extend({
                reset: function reset() {
                    this._data = new a.init,
                    this._nDataBytes = 0
                },
                _append: function _append(e) {
                    "string" == typeof e && (e = _.parse(e)),
                    this._data.concat(e),
                    this._nDataBytes += e.sigBytes
                },
                _process: function _process(t) {
                    var r = this._data
                      , n = r.words
                      , i = r.sigBytes
                      , o = this.blockSize
                      , s = i / (4 * o);
                    if (t = (s = t ? e.ceil(s) : e.max((0 | s) - this._minBufferSize, 0)) * o,
                    i = e.min(4 * t, i),
                    t) {
                        for (var c = 0; c < t; c += o)
                            this._doProcessBlock(n, c);
                        c = n.splice(0, t),
                        r.sigBytes -= i
                    }
                    return new a.init(c,i)
                },
                clone: function clone() {
                    var e = o.clone.call(this);
                    return e._data = this._data.clone(),
                    e
                },
                _minBufferSize: 0
            });
            n.Hasher = f.extend({
                cfg: o.extend(),
                init: function init(e) {
                    this.cfg = this.cfg.extend(e),
                    this.reset()
                },
                reset: function reset() {
                    f.reset.call(this),
                    this._doReset()
                },
                update: function update(e) {
                    return this._append(e),
                    this._process(),
                    this
                },
                finalize: function finalize(e) {
                    return e && this._append(e),
                    this._doFinalize()
                },
                blockSize: 16,
                _createHelper: function _createHelper(e) {
                    return function(t, r) {
                        return new e.init(r).finalize(t)
                    }
                },
                _createHmacHelper: function _createHmacHelper(e) {
                    return function(t, r) {
                        return new l.HMAC.init(e,r).finalize(t)
                    }
                }
            });
            var l = r.algo = {};
            return r
        }(Math);
        !function(e) {
            function p(e, t, r, n, i, o, a) {
                return ((e = e + (t & r | ~t & n) + i + a) << o | e >>> 32 - o) + t
            }
            function m(e, t, r, n, i, o, a) {
                return ((e = e + (t & n | r & ~n) + i + a) << o | e >>> 32 - o) + t
            }
            function l(e, t, r, n, i, o, a) {
                return ((e = e + (t ^ r ^ n) + i + a) << o | e >>> 32 - o) + t
            }
            function n(e, t, r, n, i, o, a) {
                return ((e = e + (r ^ (t | ~n)) + i + a) << o | e >>> 32 - o) + t
            }
            for (var t = i, r = (a = t.lib).WordArray, o = a.Hasher, a = t.algo, s = [], c = 0; 64 > c; c++)
                s[c] = 4294967296 * e.abs(e.sin(c + 1)) | 0;
            a = a.MD5 = o.extend({
                _doReset: function _doReset() {
                    this._hash = new r.init([1732584193, 4023233417, 2562383102, 271733878])
                },
                _doProcessBlock: function _doProcessBlock(e, t) {
                    for (var r = 0; 16 > r; r++) {
                        var i = e[c = t + r];
                        e[c] = 16711935 & (i << 8 | i >>> 24) | 4278255360 & (i << 24 | i >>> 8)
                    }
                    r = this._hash.words;
                    var o, a, c = e[t + 0], u = (i = e[t + 1],
                    e[t + 2]), _ = e[t + 3], f = e[t + 4], d = e[t + 5], h = e[t + 6], g = e[t + 7], w = e[t + 8], y = e[t + 9], v = e[t + 10], b = e[t + 11], S = e[t + 12], k = e[t + 13], x = e[t + 14], B = e[t + 15], P = r[0], D = n(D = n(D = n(D = n(D = l(D = l(D = l(D = l(D = m(D = m(D = m(D = m(D = p(D = p(D = p(D = p(D = r[1], a = p(a = r[2], o = p(o = r[3], P = p(P, D, a, o, c, 7, s[0]), D, a, i, 12, s[1]), P, D, u, 17, s[2]), o, P, _, 22, s[3]), a = p(a, o = p(o, P = p(P, D, a, o, f, 7, s[4]), D, a, d, 12, s[5]), P, D, h, 17, s[6]), o, P, g, 22, s[7]), a = p(a, o = p(o, P = p(P, D, a, o, w, 7, s[8]), D, a, y, 12, s[9]), P, D, v, 17, s[10]), o, P, b, 22, s[11]), a = p(a, o = p(o, P = p(P, D, a, o, S, 7, s[12]), D, a, k, 12, s[13]), P, D, x, 17, s[14]), o, P, B, 22, s[15]), a = m(a, o = m(o, P = m(P, D, a, o, i, 5, s[16]), D, a, h, 9, s[17]), P, D, b, 14, s[18]), o, P, c, 20, s[19]), a = m(a, o = m(o, P = m(P, D, a, o, d, 5, s[20]), D, a, v, 9, s[21]), P, D, B, 14, s[22]), o, P, f, 20, s[23]), a = m(a, o = m(o, P = m(P, D, a, o, y, 5, s[24]), D, a, x, 9, s[25]), P, D, _, 14, s[26]), o, P, w, 20, s[27]), a = m(a, o = m(o, P = m(P, D, a, o, k, 5, s[28]), D, a, u, 9, s[29]), P, D, g, 14, s[30]), o, P, S, 20, s[31]), a = l(a, o = l(o, P = l(P, D, a, o, d, 4, s[32]), D, a, w, 11, s[33]), P, D, b, 16, s[34]), o, P, x, 23, s[35]), a = l(a, o = l(o, P = l(P, D, a, o, i, 4, s[36]), D, a, f, 11, s[37]), P, D, g, 16, s[38]), o, P, v, 23, s[39]), a = l(a, o = l(o, P = l(P, D, a, o, k, 4, s[40]), D, a, c, 11, s[41]), P, D, _, 16, s[42]), o, P, h, 23, s[43]), a = l(a, o = l(o, P = l(P, D, a, o, y, 4, s[44]), D, a, S, 11, s[45]), P, D, B, 16, s[46]), o, P, u, 23, s[47]), a = n(a, o = n(o, P = n(P, D, a, o, c, 6, s[48]), D, a, g, 10, s[49]), P, D, x, 15, s[50]), o, P, d, 21, s[51]), a = n(a, o = n(o, P = n(P, D, a, o, S, 6, s[52]), D, a, _, 10, s[53]), P, D, v, 15, s[54]), o, P, i, 21, s[55]), a = n(a, o = n(o, P = n(P, D, a, o, w, 6, s[56]), D, a, B, 10, s[57]), P, D, h, 15, s[58]), o, P, k, 21, s[59]), a = n(a, o = n(o, P = n(P, D, a, o, f, 6, s[60]), D, a, b, 10, s[61]), P, D, u, 15, s[62]), o, P, y, 21, s[63]);
                    r[0] = r[0] + P | 0,
                    r[1] = r[1] + D | 0,
                    r[2] = r[2] + a | 0,
                    r[3] = r[3] + o | 0
                },
                _doFinalize: function _doFinalize() {
                    var t = this._data
                      , r = t.words
                      , n = 8 * this._nDataBytes
                      , i = 8 * t.sigBytes;
                    r[i >>> 5] |= 128 << 24 - i % 32;
                    var o = e.floor(n / 4294967296);
                    for (r[15 + (i + 64 >>> 9 << 4)] = 16711935 & (o << 8 | o >>> 24) | 4278255360 & (o << 24 | o >>> 8),
                    r[14 + (i + 64 >>> 9 << 4)] = 16711935 & (n << 8 | n >>> 24) | 4278255360 & (n << 24 | n >>> 8),
                    t.sigBytes = 4 * (r.length + 1),
                    this._process(),
                    r = (t = this._hash).words,
                    n = 0; 4 > n; n++)
                        i = r[n],
                        r[n] = 16711935 & (i << 8 | i >>> 24) | 4278255360 & (i << 24 | i >>> 8);
                    return t
                },
                clone: function clone() {
                    var e = o.clone.call(this);
                    return e._hash = this._hash.clone(),
                    e
                }
            }),
            t.MD5 = o._createHelper(a),
            t.HmacMD5 = o._createHmacHelper(a)
        }(Math),
        window.CryptoJS = i;
        var o = "//playweb.douyu.com"
          , a = "acf"
          , s = a || a
          , c = o || o
          , u = function getCookieData(e) {
            return document.cookie.match(new RegExp("(^| )" + s + "_" + e + "=([^;]*)(;|$)"))
        }
          , _ = function getRoomData(e) {
            return (window.$ROOM || {})[e]
        };
        try {
            !function preLoadStream() {
                var e = u("did")
                  , t = u("uid")
                  , r = _("owner_uid")
                  , n = u("groupid")
                  , i = _("room_id")
                  , o = +r !== +t && _("isVip") && 5 === +n
                  , a = 431460 === i
                  , s = function getLocalStory(e, t) {
                    var r = e + "_h5p_room"
                      , n = t;
                    try {
                        var i = window.localStorage.getItem(r);
                        return JSON.parse(i).v
                    } catch (e) {
                        return n
                    }
                }
                  , f = function setLocalStorage(e, t) {
                    window.localStorage.setItem(e + "_h5p_room", JSON.stringify({
                        c: 1e3 * parseInt((new Date).getTime() / 1e3, 10),
                        e: 0xe677d21fd818,
                        v: JSON.stringify(t),
                        r: 1
                    }))
                }
                  , l = function getIve() {
                    var e = s("GaoRateTimestamp", 0)
                      , t = s("rateRecordTime", 0);
                    return function isNextDay(e, t, r) {
                        var n = new Date(t);
                        return e < new Date(n.getFullYear(),n.getMonth(),n.getHours() >= r ? n.getDate() : n.getDate() - 1,r).getTime()
                    }(e, (new Date).valueOf(), 19) ? (f("rateRecordTime", 0),
                    f("realRateModel", -1),
                    0) : t >= 3 ? 1 : 0
                }
                  , p = function getStreamPostUrl() {
                    var r = function getPostStreamPostData() {
                        var r = e && e.length > 1 ? decodeURIComponent(e[2]) : "10000000000000000000000000001501"
                          , n = window.ub98484234(i, r, parseInt((new Date).getTime() / 1e3, 10))
                          , a = s("realRateModel", "-1")
                          , c = s("player_storage_cdn", "")
                          , u = l();
                        return o ? n + "&cdn=" + c + "&rate=" + a + "&ver=Douyu_222082905&iar=1&ive=" + u + "&hevc=0&fa=0&aid=web-alone&uid=" + t : n + "&cdn=" + c + "&rate=" + a + "&ver=Douyu_222082905&iar=1&ive=" + u + "&hevc=0&fa=0"
                    }();
                    return o ? c + "/lapi/live/getH5Play/" + i + "?" + r : "/lapi/live/getH5Play/" + i + "?" + r
                };
                !function requireStreamInfo() {
                    if (i && !a && !function isListPreload() {
                        try {
                            var e = localStorage.getItem("h5StreamPreload_h5p_room");
                            if (e) {
                                var t = JSON.parse(e);
                                if (Date.now() < t.e) {
                                    var r = JSON.parse(t.v);
                                    if (r && r.room_id === +i && r.multirates && r.multirates.length > 0)
                                        return !0
                                }
                            }
                            return !1
                        } catch (e) {
                            return !1
                        }
                    }() && !function isWebmRoom() {
                        return !!window.zhtName
                    }())
                        try {
                            window.getStreamInfoPromise = new Promise(function(e, t) {
                                fetch(p(), {
                                    method: "post"
                                }).then(function(e) {
                                    return e.json()
                                }).then(function(r) {
                                    0 === r.error ? e(r.data) : t()
                                }).catch(t)
                            }
                            ),
                            window.getStreamInfoPromise.then(function() {}).catch(function() {})
                        } catch (e) {
                            window.getStreamInfoPromise = void 0
                        }
                }()
            }()
        } catch (e) {}
    }
});
//# sourceMappingURL=http://sourcemap.douyucdn.cn:4567/room/online/sourcemaps/player_first_preload_stream_84e4238.js.map
