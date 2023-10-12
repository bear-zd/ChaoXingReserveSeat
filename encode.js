/*
 * A JavaScript implementation of the RSA Data Security, Inc. MD5 Message
 * Digest Algorithm, as defined in RFC 1321.
 * Version 2.1 Copyright (C) Paul Johnston 1999 - 2002.
 * Other contributors: Greg Holt, Andrew Kepert, Ydnar, Lostinet
 * Distributed under the BSD License
 * See http://pajhome.org.uk/crypt/md5 for more info.
 */

/*
 * Configurable variables. You may need to tweak these to be compatible with
 * the server-side, but the defaults work in most cases.
 */
var hexcase = 0;  /* hex output format. 0 - lowercase; 1 - uppercase        */
var b64pad  = ""; /* base-64 pad character. "=" for strict RFC compliance   */
var chrsz   = 8;  /* bits per input character. 8 - ASCII; 16 - Unicode      */

function safe_add(x, y)
{
  var lsw = (x & 0xFFFF) + (y & 0xFFFF);
  var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
  return (msw << 16) | (lsw & 0xFFFF);
}

function bit_rol(num, cnt)
{
  return (num << cnt) | (num >>> (32 - cnt));
}
function md5_cmn(q, a, b, x, s, t)
{
  return safe_add(bit_rol(safe_add(safe_add(a, q), safe_add(x, t)), s),b);
}
function md5_ff(a, b, c, d, x, s, t)
{
  return md5_cmn((b & c) | ((~b) & d), a, b, x, s, t);
}
function md5_gg(a, b, c, d, x, s, t)
{
  return md5_cmn((b & d) | (c & (~d)), a, b, x, s, t);
}
function md5_hh(a, b, c, d, x, s, t)
{
  return md5_cmn(b ^ c ^ d, a, b, x, s, t);
}
function md5_ii(a, b, c, d, x, s, t)
{
  return md5_cmn(c ^ (b | (~d)), a, b, x, s, t);
}

function core_md5(x, len)
{
  /* append padding */
  x[len >> 5] |= 0x80 << ((len) % 32);
  x[(((len + 64) >>> 9) << 4) + 14] = len;
  
  var a =  1732584193;
  var b = -271733879;
  var c = -1732584194;
  var d =  271733878;
  
  for(var i = 0; i < x.length; i += 16)
  {
    var olda = a;
    var oldb = b;
    var oldc = c;
    var oldd = d;
    
    a = md5_ff(a, b, c, d, x[i+ 0], 7 , -680876936);
    d = md5_ff(d, a, b, c, x[i+ 1], 12, -389564586);
    c = md5_ff(c, d, a, b, x[i+ 2], 17,  606105819);
    b = md5_ff(b, c, d, a, x[i+ 3], 22, -1044525330);
    a = md5_ff(a, b, c, d, x[i+ 4], 7 , -176418897);
    d = md5_ff(d, a, b, c, x[i+ 5], 12,  1200080426);
    c = md5_ff(c, d, a, b, x[i+ 6], 17, -1473231341);
    b = md5_ff(b, c, d, a, x[i+ 7], 22, -45705983);
    a = md5_ff(a, b, c, d, x[i+ 8], 7 ,  1770035416);
    d = md5_ff(d, a, b, c, x[i+ 9], 12, -1958414417);
    c = md5_ff(c, d, a, b, x[i+10], 17, -42063);
    b = md5_ff(b, c, d, a, x[i+11], 22, -1990404162);
    a = md5_ff(a, b, c, d, x[i+12], 7 ,  1804603682);
    d = md5_ff(d, a, b, c, x[i+13], 12, -40341101);
    c = md5_ff(c, d, a, b, x[i+14], 17, -1502002290);
    b = md5_ff(b, c, d, a, x[i+15], 22,  1236535329);
    
    a = md5_gg(a, b, c, d, x[i+ 1], 5 , -165796510);
    d = md5_gg(d, a, b, c, x[i+ 6], 9 , -1069501632);
    c = md5_gg(c, d, a, b, x[i+11], 14,  643717713);
    b = md5_gg(b, c, d, a, x[i+ 0], 20, -373897302);
    a = md5_gg(a, b, c, d, x[i+ 5], 5 , -701558691);
    d = md5_gg(d, a, b, c, x[i+10], 9 ,  38016083);
    c = md5_gg(c, d, a, b, x[i+15], 14, -660478335);
    b = md5_gg(b, c, d, a, x[i+ 4], 20, -405537848);
    a = md5_gg(a, b, c, d, x[i+ 9], 5 ,  568446438);
    d = md5_gg(d, a, b, c, x[i+14], 9 , -1019803690);
    c = md5_gg(c, d, a, b, x[i+ 3], 14, -187363961);
    b = md5_gg(b, c, d, a, x[i+ 8], 20,  1163531501);
    a = md5_gg(a, b, c, d, x[i+13], 5 , -1444681467);
    d = md5_gg(d, a, b, c, x[i+ 2], 9 , -51403784);
    c = md5_gg(c, d, a, b, x[i+ 7], 14,  1735328473);
    b = md5_gg(b, c, d, a, x[i+12], 20, -1926607734);
    
    a = md5_hh(a, b, c, d, x[i+ 5], 4 , -378558);
    d = md5_hh(d, a, b, c, x[i+ 8], 11, -2022574463);
    c = md5_hh(c, d, a, b, x[i+11], 16,  1839030562);
    b = md5_hh(b, c, d, a, x[i+14], 23, -35309556);
    a = md5_hh(a, b, c, d, x[i+ 1], 4 , -1530992060);
    d = md5_hh(d, a, b, c, x[i+ 4], 11,  1272893353);
    c = md5_hh(c, d, a, b, x[i+ 7], 16, -155497632);
    b = md5_hh(b, c, d, a, x[i+10], 23, -1094730640);
    a = md5_hh(a, b, c, d, x[i+13], 4 ,  681279174);
    d = md5_hh(d, a, b, c, x[i+ 0], 11, -358537222);
    c = md5_hh(c, d, a, b, x[i+ 3], 16, -722521979);
    b = md5_hh(b, c, d, a, x[i+ 6], 23,  76029189);
    a = md5_hh(a, b, c, d, x[i+ 9], 4 , -640364487);
    d = md5_hh(d, a, b, c, x[i+12], 11, -421815835);
    c = md5_hh(c, d, a, b, x[i+15], 16,  530742520);
    b = md5_hh(b, c, d, a, x[i+ 2], 23, -995338651);
    
    a = md5_ii(a, b, c, d, x[i+ 0], 6 , -198630844);
    d = md5_ii(d, a, b, c, x[i+ 7], 10,  1126891415);
    c = md5_ii(c, d, a, b, x[i+14], 15, -1416354905);
    b = md5_ii(b, c, d, a, x[i+ 5], 21, -57434055);
    a = md5_ii(a, b, c, d, x[i+12], 6 ,  1700485571);
    d = md5_ii(d, a, b, c, x[i+ 3], 10, -1894986606);
    c = md5_ii(c, d, a, b, x[i+10], 15, -1051523);
    b = md5_ii(b, c, d, a, x[i+ 1], 21, -2054922799);
    a = md5_ii(a, b, c, d, x[i+ 8], 6 ,  1873313359);
    d = md5_ii(d, a, b, c, x[i+15], 10, -30611744);
    c = md5_ii(c, d, a, b, x[i+ 6], 15, -1560198380);
    b = md5_ii(b, c, d, a, x[i+13], 21,  1309151649);
    a = md5_ii(a, b, c, d, x[i+ 4], 6 , -145523070);
    d = md5_ii(d, a, b, c, x[i+11], 10, -1120210379);
    c = md5_ii(c, d, a, b, x[i+ 2], 15,  718787259);
    b = md5_ii(b, c, d, a, x[i+ 9], 21, -343485551);
    
    a = safe_add(a, olda);
    b = safe_add(b, oldb);
    c = safe_add(c, oldc);
    d = safe_add(d, oldd);
  }
  return Array(a, b, c, d);
  
}

function binl2hex(binarray)
{
  var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef";
  var str = "";
  for(var i = 0; i < binarray.length * 4; i++)
  {
    str += hex_tab.charAt((binarray[i>>2] >> ((i%4)*8+4)) & 0xF) +
        hex_tab.charAt((binarray[i>>2] >> ((i%4)*8  )) & 0xF);
  }
  return str;
}
function str2binl(str)
{
  var bin = Array();
  var mask = (1 << chrsz) - 1;
  for(var i = 0; i < str.length * chrsz; i += chrsz)
    bin[i>>5] |= (str.charCodeAt(i / chrsz) & mask) << (i%32);
  return bin;
}

function hex_md5(s){ return binl2hex(core_md5(str2binl(s), s.length * chrsz));}



var encode_version = 'jsjiami.com.v5',
    iuwen = '__0x10376c',
    __0x10376c = ['w7vDjUE=', '5Yql6Zib54me5p+95Yyn772jFQnkv4Plr4zmnaDlvobnq7c=', 'w4TDl8OUwqYUw7dCC1s=', 'YMKLw7zDsHg=', 'woLCthHDncOQ', '54mV5p+w5Yyg77+uOMKJ5Lyi5a2v5pyg5byQ56mU77yl6L+b6K2Z5paz5o+Z5oiV5LiX55ic5baQ5L21', 'w43DukAsdQ==', 'QFcO', 'wozDl8OLLw==', 'asOfIi0=', 'wo4qw74=', 'wrvCtCo=', 'AsOERsOzw4U=', 'AcOGCnfCkQ==', 'M8ONdXnCpQ==', 'XMODGkIUw6jDlcOsw44Mw6c3MC9Nwo8YSA==', 'wrtHwrFk', 'woR+wq5rfQ==', 'bQxsw57CkA==', 'woPCnxDDi8Oc', 'EcKNwr5twoc=', 'w4nDi8OtEsOhw5U='];
(function (_0x5427f1, _0x3f895b) {
    var _0xf670e7 = function (_0x2797ef) {
        while (--_0x2797ef) {
            _0x5427f1['push'](_0x5427f1['shift']());
        }
    };
    _0xf670e7(++_0x3f895b);
}(__0x10376c, 0x1a9));
var _0x4407 = function (_0x3b8d67, _0x237f78) {
    _0x3b8d67 = _0x3b8d67 - 0x0;
    var _0x9e1d38 = __0x10376c[_0x3b8d67];
    if (_0x4407['initialized'] === undefined) {
        (function () {
            var _0x4a2c11 = typeof window !== 'undefined' ? window : typeof process === 'object' && typeof require === 'function' && typeof global === 'object' ? global : this;
            var _0x676be2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
            _0x4a2c11['atob'] || (_0x4a2c11['atob'] = function (_0xff241) {
                var _0x3cc5dc = String(_0xff241)['replace'](/=+$/, '');
                for (var _0xcce26b = 0x0, _0x57f217, _0x16ae35, _0x228e91 = 0x0, _0x56b988 = ''; _0x16ae35 = _0x3cc5dc['charAt'](_0x228e91++); ~_0x16ae35 && (_0x57f217 = _0xcce26b % 0x4 ? _0x57f217 * 0x40 + _0x16ae35 : _0x16ae35, _0xcce26b++ % 0x4) ? _0x56b988 += String['fromCharCode'](0xff & _0x57f217 >> (-0x2 * _0xcce26b & 0x6)) : 0x0) {
                    _0x16ae35 = _0x676be2['indexOf'](_0x16ae35);
                }
                return _0x56b988;
            });
        }());
        var _0x5e441c = function (_0x30df10, _0x1d34ce) {
            var _0x2cac87 = [],
                _0x2ae2c4 = 0x0,
                _0x3201e7, _0x37b644 = '',
                _0x11190b = '';
            _0x30df10 = atob(_0x30df10);
            for (var _0x222f3d = 0x0, _0x32b2bd = _0x30df10['length']; _0x222f3d < _0x32b2bd; _0x222f3d++) {
                _0x11190b += '%' + ('00' + _0x30df10['charCodeAt'](_0x222f3d)['toString'](0x10))['slice'](-0x2);
            }
            _0x30df10 = decodeURIComponent(_0x11190b);
            for (var _0x3a744a = 0x0; _0x3a744a < 0x100; _0x3a744a++) {
                _0x2cac87[_0x3a744a] = _0x3a744a;
            }
            for (_0x3a744a = 0x0; _0x3a744a < 0x100; _0x3a744a++) {
                _0x2ae2c4 = (_0x2ae2c4 + _0x2cac87[_0x3a744a] + _0x1d34ce['charCodeAt'](_0x3a744a % _0x1d34ce['length'])) % 0x100;
                _0x3201e7 = _0x2cac87[_0x3a744a];
                _0x2cac87[_0x3a744a] = _0x2cac87[_0x2ae2c4];
                _0x2cac87[_0x2ae2c4] = _0x3201e7;
            }
            _0x3a744a = 0x0;
            _0x2ae2c4 = 0x0;
            for (var _0x33b43b = 0x0; _0x33b43b < _0x30df10['length']; _0x33b43b++) {
                _0x3a744a = (_0x3a744a + 0x1) % 0x100;
                _0x2ae2c4 = (_0x2ae2c4 + _0x2cac87[_0x3a744a]) % 0x100;
                _0x3201e7 = _0x2cac87[_0x3a744a];
                _0x2cac87[_0x3a744a] = _0x2cac87[_0x2ae2c4];
                _0x2cac87[_0x2ae2c4] = _0x3201e7;
                _0x37b644 += String['fromCharCode'](_0x30df10['charCodeAt'](_0x33b43b) ^ _0x2cac87[(_0x2cac87[_0x3a744a] + _0x2cac87[_0x2ae2c4]) % 0x100]);
            }
            return _0x37b644;
        };
        _0x4407['rc4'] = _0x5e441c;
        _0x4407['data'] = {};
        _0x4407['initialized'] = !![];
    }
    var _0x255660 = _0x4407['data'][_0x3b8d67];
    if (_0x255660 === undefined) {
        if (_0x4407['once'] === undefined) {
            _0x4407['once'] = !![];
        }
        _0x9e1d38 = _0x4407['rc4'](_0x9e1d38, _0x237f78);
        _0x4407['data'][_0x3b8d67] = _0x9e1d38;
    } else {
        _0x9e1d38 = _0x255660;
    }
    return _0x9e1d38;
};

function _0x4aac3d(_0xfd3213) {
    var _0x4e1fea = Object[_0x4407('0x1', '6E&f')](_0xfd3213)[_0x4407('0x2', '9bu%')]();
    var _0x30ab3a = {};
    for (let _0x529462 = 0x0; _0x529462 < _0x4e1fea['length']; _0x529462++) {
        _0x30ab3a[_0x4e1fea[_0x529462]] = _0xfd3213[_0x4e1fea[_0x529462]];
    }
    return _0x30ab3a;
}

function _0xd5d9ff(_0x1a35a1) {
    var _0x5f1401 = {
        'vVhWL': function _0x193d40(_0x384730, _0x16064b) {
            return _0x384730 !== _0x16064b;
        },
        'QDtun': _0x4407('0x3', '7%p#'),
        'ZyxHo': _0x4407('0x4', 'isfk'),
        'NnIBP': function _0x220eb3(_0x96bdaa, _0x220d20) {
            return _0x96bdaa(_0x220d20);
        },
        'OLlgO': function _0x28d265(_0x597f06, _0x95c23) {
            return _0x597f06 + _0x95c23;
        },
        'ndHxm': function _0x59e9f6(_0x404294, _0x2adbc2) {
            return _0x404294 + _0x2adbc2;
        },
        'RGnnK': function _0x19779b(_0x461ef0, _0x3da61a) {
            return _0x461ef0 + _0x3da61a;
        }
    };
    if (_0x5f1401[_0x4407('0x5', 'IaWk')](_0x5f1401[_0x4407('0x6', 'jAbf')], _0x5f1401[_0x4407('0x7', 'zcTz')])) {
        var _0x16263b = _0x4407('0x8', '68^S');
        var _0x4299a1 = _0x5f1401['NnIBP'](_0x4aac3d, _0x1a35a1);
        var _0x443159 = [];
        for (var _0xdf82cf in _0x4299a1) {
            _0x443159[_0x4407('0x9', '^TE9')](_0x5f1401[_0x4407('0xa', '^TE9')](_0x5f1401[_0x4407('0xb', 'zmY9')](_0x5f1401['RGnnK']('[', _0xdf82cf), '='), _0x4299a1[_0xdf82cf]) + ']');
        }
        _0x443159['push'](_0x5f1401[_0x4407('0xc', 'isfk')](_0x5f1401[_0x4407('0xd', 'IquD')]('[', _0x16263b), ']'));
        var _0x2f67c8 = '';
        for (var _0x130b05 = 0x0; _0x130b05 < _0x443159[_0x4407('0xe', 'cc%F')]; _0x130b05++) {
            _0x2f67c8 += _0x443159[_0x130b05];
        }
        return hex_md5(_0x2f67c8);
    } else {
        newObj[newkey[_0x130b05]] = arys[newkey[_0x130b05]];
    }
};

    
 function verifyParam(objectParm){ return _0xd5d9ff(objectParm)}   ;

(function (_0x10220a, _0x4f7412, _0x347bdf) {
    var _0x347b20 = {
        'WRPdK': _0x4407('0xf', 'Qsxt'),
        'LBmEm': function _0x35d933(_0x5987f6, _0x31faff) {
            return _0x5987f6 === _0x31faff;
        },
        'Hjkxa': 'jsjiami.com.v5',
        'SnoxG': function _0x5f43c2(_0x7c6480, _0x44deec) {
            return _0x7c6480 + _0x44deec;
        },
        'hGkea': _0x4407('0x10', 'Ecxc')
    };
    _0x347bdf = 'al';
    try {
        _0x347bdf += _0x347b20['WRPdK'];
        _0x4f7412 = encode_version;
        if (!(typeof _0x4f7412 !== _0x4407('0x11', 'ab9u') && _0x347b20[_0x4407('0x12', 'Z4f7')](_0x4f7412, _0x347b20['Hjkxa']))) {
            _0x10220a[_0x347bdf](_0x347b20[_0x4407('0x13', 'isfk')]('删除', _0x4407('0x14', '^vb!')));
        }
    } catch (_0x2887b6) {
        _0x10220a[_0x347bdf](_0x347b20[_0x4407('0x15', 'y7Pe')]);
    }
}(window));;
encode_version = 'jsjiami.com.v5';

verifyParam({
    "roomId": "roomIdparm",
    "day": "dayparm",
    "startTime": "startTimeparm",
    "endTime": "endTimeparm",
    "seatNum": "seatNumparm",
    "captcha": "",
    "token": "tokenparm",
    "type": 1,
    "verifyData": 1
})