
print("hellword bestV8");

function v(t) {
    var n = t.SIGN;
    t = t.str,
        t = decodeURI(t),
        n = d.a.HmacSHA1(d.a.enc.Utf8.parse(t), n),
        n = d.a.enc.Base64.stringify(n).toString();
    return f()(n)

}

t = {
    SIGN: "D23ABC@#56",
    str: "api.eol.cn/web/api/?keyword=&page=6&province_id=&ranktype=&request_type=1&size=20&top_school_id=1169,1159,435,457,436,589,459,3269,3117,434,1551,3374,3375&type=&uri=apidata/api/gkv3/school/lists"
}


var result = v(t)

result;