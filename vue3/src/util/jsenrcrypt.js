import JSEncrypt from "jsencrypt";


//生成密钥对 http://web.chacuo.net/netrsakeypair

const publicKey = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArnAGX1amynx1kg7/SVtz\n' +
    'Pj2DMKzEDAclI15b12eulMsrlPhka19y0j56U4Y2Zoew9p2MsBGSTB3aZMt4g68J\n' +
    'dF5TlUPlKMJrloH4eEJhfLpFumBskRrd1QuH64kiIjZfP3i/02GNFq0Q+WVKCVIb\n' +
    'UeSUYbDjxg0MYLSJPaSZvl5pQNiXPZaOSgu1/ZJoKQgxglU1bzdblY/mv+cIBqWu\n' +
    'lJjt9FbXaU64OUBZ+CA4f9sWcS6GTk4o0FCL9vqz/Kxn5F1NLcmg2mqq2RkShC8v\n' +
    '5hq4eCz2xPDdBgOLkA6KoT7gy6Ruy77RKvm6CFBswNznwWqXS570HlkWZMVqlCBb\n' +
    'PwIDAQAB'


const privateKey = 'MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCucAZfVqbKfHWS\n' +
    'Dv9JW3M+PYMwrMQMByUjXlvXZ66UyyuU+GRrX3LSPnpThjZmh7D2nYywEZJMHdpk\n' +
    'y3iDrwl0XlOVQ+UowmuWgfh4QmF8ukW6YGyRGt3VC4friSIiNl8/eL/TYY0WrRD5\n' +
    'ZUoJUhtR5JRhsOPGDQxgtIk9pJm+XmlA2Jc9lo5KC7X9kmgpCDGCVTVvN1uVj+a/\n' +
    '5wgGpa6UmO30VtdpTrg5QFn4IDh/2xZxLoZOTijQUIv2+rP8rGfkXU0tyaDaaqrZ\n' +
    'GRKELy/mGrh4LPbE8N0GA4uQDoqhPuDLpG7LvtEq+boIUGzA3OfBapdLnvQeWRZk\n' +
    'xWqUIFs/AgMBAAECggEAHTLPPkIo5Rf0LiCohsTyA2cUgJ9KqaDAjK0Mvn+yb2Ga\n' +
    'x/LUDE0L0Tl4DGcY0AzCiGVS2V33mRoeJmUQpSo1cO8hGokk4K+6hpT23FpwKwqb\n' +
    'BVmCkr9mhnTJqZlox0VGqD80DNP1Y+hQQQ69V9YQkKKsW7XaSpqAieduWY0l1wF7\n' +
    '3i3z1i8zXwZxvqJbLLJ0jFh37RrimcES9GuHGKLNoP6vgC+KFN0JklITJAcUk4V4\n' +
    'ngCa1hGpKPVLzoPdzUsybR6Pz0WQ+9PQKLKwvPWJOwbV+1qH1AQrENcs6L/owPqn\n' +
    'dRYv4RM63gRz7p9OHShcN/WN+X6uIOTCmWq+tJG4IQKBgQDbGhYcKSSCTcMTef+a\n' +
    'wDcIhmyN4jIMdirOmdatyrHiTFZ1TgsdQH39JGgZV1xXMqLRQlZgRrfAQVGApvj+\n' +
    'gc2aTQckCN1RgIQGESEAzByUKPHLKxY2T4X7LNUlBvrEyft1h0HmSkRi4Zd9obSH\n' +
    '247gm+ntENZqx92Chuc3dTH19wKBgQDL0F9k6DjiEW5IIV8j3pS8i2ddWeUojlf2\n' +
    'dnhB3gCgdhW/SrMZ4DaPgQpYSebqzw/xF0rxpagRl8KVy4KohkgmZunznU6A4pY6\n' +
    'E0dtENZ9S46OgR31X29KdxHLxTgkePOZMvv4fav/pKUSjpQhF785T+70RlfIrsRO\n' +
    'Og/bTHlS+QKBgQCiETi7md9Ml3KtzHc6o+XRY4WWqfN1bk8ZxYebxCwyhV8KpDDq\n' +
    'cVMAVda+r/U49taizVwRGR5AktBTxq61q5RHB6U5jWkQKWz/A9qSuWiGW4cHTpa+\n' +
    'k7I6ah47pl8GA5YCiItBajwNnGsvXdapC8oy8IFnfyXrlG2QaHNNfV34XwKBgGNH\n' +
    '2XAZ/ruAqivQtbuPTPybG3rJs2sSC58vDl1nev6vBuDrzlqocWtt/FANj8KJosZa\n' +
    'BlO30irfthWp0Leu0a6DKytUUU1PEsavZXenYBQgngyksKc6Gcg4QB72ruZ1VJQn\n' +
    '1b2x2frphM+JTHbiTm/olAnByjkjiNRiTB8THXZhAoGBAMBC5LZbD5+ksVDtaKyF\n' +
    '8/kRVIXuksA4SQjGiXH46MGS2ifnBlPOB42Xad9WwFNAczxoFOnOX0Hewgz+I0RM\n' +
    '+4bEjQ4iFBFAArjT+2ZP1hpNAZ9NK9LOIo1hRKA/y2z+RRJj+hpWlvIkrgXqxa41\n' +
    'ul0XmgonuwL9AFii6aOQfX/7'


//加密
function encrypt(text) {
    const encryptor = new JSEncrypt()
    encryptor.setPublicKey(publicKey)
    return encryptor.encrypt(text)
}

//解密
function decrypt(text) {
    const decryptor = new JSEncrypt()
    decryptor.setPrivateKey(privateKey)
    return decryptor.decrypt(text)
}

export {
    encrypt,
    decrypt
}


