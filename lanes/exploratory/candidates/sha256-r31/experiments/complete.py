"""Completion step P5 (proof.md Section 4) on organizer seeds.

Each embedded pair (M0, M1) is one of this package's certificates: M0 is a random first block whose
chaining value matched a table entry, and M1 holds the message words W0..W12 and W14 that the
attack derived for it. For every organizer trial this program keeps W0..W12 and W14, draws E13 and
E15 from the trial seed, solves W13 and W15 from the step equations so that steps 13..17 of the two
messages follow the characteristic, and returns the new pair M0||M1, M0||M1' with M1' = M1 + dW
on words 5..9. It also re-checks that steps 0..12 of both messages follow Table 6.
"""
import hashlib
import json
import sys

MASK = 0xFFFFFFFF
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351]
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
DW = {5: 0xfffff006, 6: 0x002087f1, 7: 0x4fefb5fa, 8: 0x28011100, 9: 0x00008004}
DW16 = 0x00008004

# Table 6 rows (A_i, E_i) for i = 5..14; position k is bit 31-k; '=', '0', '1' mean no difference.
ROWS = {
    5: ("===================n=unnnnnnn=n=", "000111010001111110nu=11111unnnu1"),
    6: ("========n======================u", "101011=11==0n0==u11110==1110011n"),
    7: ("===u===n==n========n=========n=u", "un0u1100n=01u11111001u1=n110u10n"),
    8: ("=============================n==", "1u01un0u0=1=1=11n=0=u0=001001u0="),
    9: ("================================", "01100001110=0=010===00=11101u0=1"),
    10: ("================u============u==", "=1n1uuuuu0100=1un0=10unnnnnnn010"),
    11: ("================================", "=01u1010uu1==11100===1000001n=0="),
    12: ("================================", "==110001=11====1n====0011110n=0="),
    14: ("================================", "================u===========0u=="),
}


def signed(row):
    """XOR mask and the first message's bit values on it ('u' = 0 -> 1, 'n' = 1 -> 0)."""
    d = v = 0
    for k, c in enumerate(row):
        b = 31 - k
        if c in "un":
            d |= 1 << b
            if c == "n":
                v |= 1 << b
    return d, v


XE14, VE14 = signed(ROWS[14][1])

# Certificate pairs: (first block M0, second block M1), 64 bytes each, hex.
PAIRS = [
    ("8942948df3ac92e4a6b1f2c11b100164c5c6f86686d3ac169b2bceceec91ead3ebe41dc6fe76647de97637f56c6386daa82fb757e58addf90c921aecfae24660",
     "7dc1d321b62b27a388b49a735d13f83cd731a150fdbcb17381c15112237af63b63791d3aeea313db1040b07d36f6eb5f2d4d661fa330c6f0d42565fc604922f3"),
    ("39cb77de4afcd6b1c532a35c204f911a9eb808b8f5c256a9cee15844a7ca0bf43ebfe2e358aa45e6a9eca8ed5d70eafcf8fd342938c6e401150703e56737c629",
     "c8b0f702b4875d5268565f19ece8298602064d030bf63faf89937394003cd2faf79d5dfde2e3485959cb33f6970f4ed665e29b19b3edb56cb35edaf1e014aebb"),
    ("f84d171d5efdea737ebaed67fbaa217d40048a7f8dbffcab35eac992d3033881181b3eb030a8a4cdf1f166c44681b509ca86d423f8b4b14b3c93d9089ea787c7",
     "abe5cfd6702ebc17b53fbb8068f9f4d6004c2f7ce966b6b7131031b2883dd2bb65b915fee4a7515b23d3e17b30fbd056affad2904b90169934ecdc87fa280f81"),
    ("839458dc8444c76d2dd635a38aa49108c4e09a2a9336919e9ffd5b3d6165cecb0021d796b9d4b1b95888569af591a0b73e684e369b95d32aed69b33c2e3a4f22",
     "f7ab3074d6c62c1b54d07006a5f78c5697cdd36619ccb5a273582656001cd2aab8a8ef56e4b7525bebbefc099d1806e4840bb30cf251645056855b40f6c07f13"),
    ("c35ff330e6ef80d6d276aa570ab432c38b398a66dee5a0f21c48173393292bdddcaa2ecaf06f8817aee1b2c7a14c20625c4ee0a2e69c15e3648d4c157494df6b",
     "a1763eaba12e2442937c6816c2dc11e39273268a922adf26a346655cadd3732a25fc33fae2a75a5b21b1e27b30fbd056affad2904c6bbdfaf5c8db9371b257af"),
    ("0a4e550bdbaceb61d9a34af788d851a216ebc98129a05e5286f2ca6e2ef4747a1b1fc212d2b739161c36d2e49764864183b9ff0db046efb34c5c90606c481040",
     "4c5ad542bdffd0557a5402ed652dfe901476b2c3a89bb4d6645d565c237af61ae67d51bae4b351db0e31b07d3706eb5f2d5d661f4335d9001518979756c94fa7"),
    ("4acc754ad7adff20b7256cdedd85d18786b25be4ccf346536d4f541f3a2d2d778166caede0fb1c38967ae400a0ff11c815959debb944ac102908a7b7d28540b6",
     "9b66bc382a302fe000889952f2b7364dbb2c8351aa0834b7670854fa27f2777a39ba6af9e0a758d951d2557870c767d1e3c265da59b9c6a05ffefccb3f0526f2"),
    ("65b235a444deb8cf661cd67e358eb0522d27f9b212379ac1f9c565b45527027f477433bb42b9551c7da6e0b6091d40f7f92da7b6b3b2d17909de10859383a4cc",
     "5d4734778f526329504137a01b69f7e3a8f0a9982a2739a72c50533a25d2732bbdee24f8eaa71c5b0e00b17d36f6eb5f2d51661f453ec0cf7940f5541e1a36f4"),
    ("9be52073287296f3f865af1eca9d63c03a26a907a9f24595f63e645e9eeccf1621101308cb6bf12ec8bcad4ce58307161f5b04980c159491ffd3b46f812a0d35",
     "a4e1f7172c0fbc66906e2ca1d8432c40938f484ce8aa9f234dcd12348c9553ebe4fd5d7aec97145b23d3e27b30ebd056afead290697a1a1a4468b007b1c90197"),
    ("d37923df405cc658008ee9d41601010701c7a2c5e7f43cc023dee4b984d7573069d1359e3b163075d248a155cd40c557d87bf11dbe6ae1bfc5b3429f9816907f",
     "2eebefe93f609bd354bbc32ec4555a865266cdbb9d9154abce4b2014049453dae5519523e8e30b59a78b43da1735a3b095f19002c6f8dbf0b4af908659db0954"),
    ("414ada6eae87145a7d704cf23bd1d0eb40db298ae713bd59b95fec63acac2b7bde4acdedda948336bb07a7b09c9044ff724bbbb6b3b50141946f1f22c68a5dd9",
     "149861e5a42768b850c289f559155655d358d8b1b4c6924a9dc42778afd3772b351a3338e5a350db450afc777b0e5d51c392f54f0add4bcb9163cabc52453ce2"),
    ("31e973ce8afd92a96d41e3cc558c130be198a9ed10b043fe890c1cf953861a80709db6b5bef780987d4b4999c8c4994a6eaa02f8ad52e8fd84b2d04d950b6680",
     "c9d2e288b07ec8b0f5e0adb7275c7cc42b4fe3d84a617f06080311948e9557cb657919bce2a75a5b21d4e27b30fbd056affad2900c760a7757ee3879c996fbae"),
    ("cb347c8d48449734eb23531aaa3a933c2b99a91a93179cc833ad81f181f086b2d47a8b3f6dc551e90663810a57be44883e131a0107039c75888326861df40a12",
     "fdd6aca0851a3a89f6f64a4e64e83495a5486d3aa8ae7d92ec0f1292217af21a6519193de0e3485957ea33f6970f4ed6a7e25b19c98843df72bea7453274655b"),
    ("f3b5c793f26928dccdc64d8ddad302566a48f1d22bf854b19f9ca858be92870823a360061fb0e746974e9708e368c826e9f4d0364339f4164f81db202cd47285",
     "7d11b6bae29490b3ec4552d0fe2f2c4bf169b30437e63e72f14c523825d2734b36fa337ce3a34bdb4309ff777b0e5d51c392f54f55c25cd3afef767eee1c1b82"),
    ("749b094e6021acdc961b5885ac19ef749f8081aafcf8aa299814f13d9101379fd4fd323094f64454097c3ddc269432a753855302265ed92477b8e4d30a10a190",
     "f47497a8764afa9ae2700a0da64b79a0ec3df58f060e73caa90337fc27f2771a76d919fde6d712d957ac33f697034ed6a7d65b19e3927b06a16b486157cc9bf9"),
    ("f2679209aefcff6d7cd57dd39319c3e8a2ec0a6f5a90a9bb7f688628853add241a1f619ea07af8dd02479a6c04580e58d3102844f19c99148ce91265f22be8b4",
     "4a3bf61be02753cd52e41fd9600fc96b7c71f2e6a0f11d032d955190003cd2cb1a94ca67e0f758d9a9be42da1745a3b096059002880cfc90799f388e3a7c3970"),
]

# The 65 base starting points of the advice (proof.md Section 4): E5..E12 then A5..A8, hex words.
BASES = [
    "1d1fafdd ad8a7be7 4cd7cae5 946f8048 61c121d3 f02293fa 2a273419 31e3a1ec 052fb3fa 0c800b56 67601b9c 063a6fc6",
    "1d1fafdd afea7ae7 4cd7cae5 947b8048 61d131d3 7026b3fa aa372419 71f5c1e8 062f93fa cfca1ec4 a12d7e06 a33e7e34",
    "1d1fa7dd ade97ae7 4c97cbe5 942b8248 61d543d1 f02293fa aa271c18 7165d9ec 056fbbfe 6e96a692 2f69185c 2e684dee",
    "1d1fa7dd afa97be7 4c97cbe5 947bc049 61c151d1 f02293fa 2a273c18 31ef91ed 052fb3fe c49bf658 272d1f14 423ff806",
    "1d1fa7dd afaa7be7 4c97cbe5 947bc049 61d111d1 f02293fa 2a3f1418 3167d9ed 056fb3fe 8edb3712 0161fe56 48283fa4",
    "1d1fa7dd afaa7be7 4c97cbe5 947bc049 61d111d1 f02293fa 2a3f1418 3167d9ed 056fb3fe 8edb3712 0161fe56 c63e7fa4",
    "1d1fafdd adeb7ae7 4cd7cae5 946b8048 61d121d1 7026b3fa 2a370c19 31fbe9e8 052fbbfe 289846a8 012bf866 8e794d54",
    "1d1fafdd ada878e7 4c97cbe5 947bc049 61c141d1 7026b3fa aa2f141d 71e9a9ed 052fb3fe 6c9ee788 2b219944 cc3d2806",
    "1d1fa7dd afab7be7 4c97cbe5 946b8048 61c101d1 f02293fa 2a271419 b16bc9ec 056fb3fe e0d6c34a 6d64db84 ee2befc6",
    "1d1fafdd adcb78e7 4cd7cae5 947fc049 61c151d1 f02293fa 2a373418 71f1f9e9 052fb3fe 82d6b742 27613e06 2c22bed6",
    "1d1fafdd afa878e7 4c97cbe5 947fc049 61c151d1 7026b3fa 2a272c19 31ef81ed 052fb3fe ca9802d2 476cbb96 847b8f5e",
    "1d1fa7dd afab79e7 4c97cbe5 947fc049 61d101d1 f02293fa 2a3f241d 3167b1ed 062f93fe 0dd3c3a8 c3269ae4 077e4896",
    "1d1fa7dd af8b7ae7 4cd7cae5 942f8248 61d103d1 f02293fa 2a273419 f1e9c9ed 066f93fe 6bd26218 e52cfade c1748fd6",
    "1d1fafdd ad8879e7 4cd7cae5 947f8048 61c561d3 7026b3fa 2a2f141c 31fbc9e8 052fbbfa ac88ae54 a32db916 8e62cb66",
    "1d1fafdd afca7be7 4c97cbe5 946bc049 61c101d1 7026b3fa 2a3f0419 31ef89ed 066f9bfe ad9e16e2 a36bb82e 0d38bda4",
    "1d1fafdd ade87be7 4c97cbe5 942b8248 61d503d1 f02293fa 2a3f1c1c f1e989ed 056fb3fe 8c9ca362 e3621ba4 087d0bb4",
    "1d1fafdd afcb7be7 4cd7cae5 947fc049 61d501d1 f02293fa aa3f1c18 7171d9e9 062f9bfe 239d9252 416c7c9e e16b1e8e",
    "1d1fafdd af8b7be7 4c97cbe5 947fc049 61c511d1 f02293fa aa2f1c1c b1efb1ed 062f9bfe a5d33742 2764bf8e 0b6adfa4",
    "1d1fa7dd adca79e7 4c97cbe5 947f8048 61c551d3 f02293fa aa3f1419 71f1a9e8 056fb3fa ee8e6f8c 0b20b8c6 2a37ef2e",
    "1d1fafdd af8b7be7 4c97cbe5 947fc049 61c511d1 f02293fa aa2f1c1c b1efb1ed 062f9bfe a5d33742 2764bf8e 61641fa4",
    "1d1fafdd af8b7be7 4c97cbe5 947fc049 61c511d1 f02293fa aa2f1c1c b1efb1ed 062f9bfe a5d33742 2764bf8e 8b6adfa4",
    "1d1fafdd ada87ae7 4c97cbe5 946f8048 61d121d1 7026b3fa 2a3f1419 b1e3d9ed 052fbbfe e6dba2c0 cf29ba0e 2e3e6ebc",
    "1d1fafdd af8a7ae7 4c97cbe5 946f8048 61c501d1 7026b3fa aa273c1c b1f3d9e9 066f93fe 439f0320 c727ba6e c3376fc4",
    "1d1fa7dd af8878e7 4cd7cae5 947fc049 61d121d1 7026b3fa aa37141d 317fd9e9 052fbbfe ea97a260 672b1b24 ac768fce",
    "1d1fafdd afc87ae7 4c97cbe5 943b8248 61d543d1 f02293fa 2a2f241c b163c1ed f99073ff babe0472 27fa94b4 d6c6c1a5",
    "1d1fafdd afeb79e7 4cd7cae5 947b8048 61c131d1 f02293fa 2a27341d 31f7b9e8 062f93fe 8ddf522a cd6f5b6c 057218a4",
    "1d1fafdd ad8b7ae7 4c97cbe5 946fc049 61c521d1 7026b3fa 2a371418 f171f1e8 052fb3fe 2a979272 c76f3d3e 2678d8f4",
    "1d1fa7dd afc879e7 4c97cbe5 946b8048 61c161d1 f02293fa 2a2f2c19 f1f199e9 fa9053ff 91b560da 43fd1614 9bdc4335",
    "1d1fafdd af8a79e7 4c97cbe5 946fc049 61c111d1 7026b3fa 2a372419 b1fbc1e8 056fb3fe c29283c2 c7603c86 08680afe",
    "1d1fafdd adea7be7 4c97cbe5 943bc249 61d543d3 7026b3fa 2a37241d 3163b9ed f99073fb 54e30c24 8bbb936c 1891a135",
    "1d1fa7dd afa879e7 4c97cbe5 943bc249 61d523d3 f02293fa aa270c1c f1e5e9ed f9d073fb 52e91944 43b11004 b4933147",
    "1d1fafdd ade978e7 4cd7cae5 947f8048 61d101d3 f02293fa 2a273c1d 71e591ed 062f9bfa 09ca2f86 8d615944 ab7a4f6e",
    "1d1fafdd af8a7be7 4cd7cae5 943bc249 61d523d1 f02293fa 2a273c1c f1eda9ec fad05bff 3bf71160 6fb611a4 df9971a7",
    "1d1fa7dd afa87ae7 4c97cbe5 946f8048 61d511d1 f02293fa aa2f1c19 f1f981e8 056fb3fe 4cdd42ca 61685b8c e63ceef4",
    "1d1fafdd ad8878e7 4cd7cae5 947f8048 61d521d1 7026b3fa 2a3f2c18 b17bb1e9 052fbbfe ae9ca2c2 43691a04 ea7e4e84",
    "1d1fa7dd ade87ae7 4c97cbe5 943bc249 61c543d1 f02293fa aa372c1c b1fbf1e9 f9907bff 1afb8420 29bed4ec feda47f7",
    "1d1fafdd afea7be7 4cd7cae5 947f8048 61d561d3 f02293fa aa2f2c18 f179c1e9 052fbbfa c68dee4c 292cf886 4a65cd34",
    "1d1fafdd af887be7 4cd7cae5 943b8248 61d523d1 7026b3fa aa3f341d f1edd9ec fad053ff 9dffe5fa 01f35334 1986231f",
    "1d1fa7dd afc97be7 4c97cbe5 943b8248 61c523d1 f02293fa 2a3f0c1d 317bf1e8 fa905bff d5f9b072 6dfb573c d18d356d",
    "1d1fafdd afc87be7 4c97cbe5 943bc249 61d573d1 7026b3fa 2a3f2c1c f1fda9e9 056fb3fe 269c9652 056c7e9e a226781e",
    "1d1fafdd afa979e7 4c97cbe5 942bc249 61c503d1 7026b3fa 2a371c19 f1fd91e9 f9d07bff 52baf008 41bcd6c4 70d192e5",
    "1d1fa7dd ade878e7 4c97cbe5 946b8048 61d161d1 f02293fa aa370c18 b1f7e9e8 fa9053ff 1bbd0492 05fdd254 9d95276f",
    "1d1fa7dd ade878e7 4c97cbe5 946b8048 61d161d1 f02293fa aa370c18 b1f7e9e8 fa9053ff 1bbd0492 05fdd254 fd99276f",
    "1d1fa7dd adea78e7 4cd7cae5 947f8048 61c511d1 f02293fa 2a2f2418 b173b9e8 052fb3fe 2494a602 2968d8cc 6823ab5c",
    "1d1fafdd ada978e7 4c97cbe5 947fc049 61d531d1 f02293fa 2a370418 f1e5b1ec f9907bff f2fa7068 43ba16ac 14d310c5",
    "1d1fafdd af8b78e7 4cd7cae5 946f8048 61c121d3 7026b3fa aa371418 316be9ec 052fbbfa a8c5be66 2d6adeac ea61dd94",
    "1d1fafdd adca7be7 4cd7cae5 947f8048 61c101d3 7026b3fa 2a373418 31fbd9e8 062f9bfa eb856f2c 0723386e 4d7b8e34",
    "1d1fa7dd afcb7ae7 4c97cbe5 943bc249 61c553d3 7026b3fa aa3f0419 b167c9ed 066f9bfa 69862e96 056c79de 23236e0e",
    "1d1fafdd afe97be7 4c97cbe5 946b8048 61c111d3 f02293fa aa2f3419 71f1b1e8 056fbbfa e6c51f54 8f25381e 082cbbdc",
    "1d1fa7dd ada878e7 4cd7cae5 947f8048 61c131d3 f02293fa aa2f0c18 b1ffe9e9 062f93fa 67cf1a54 ed297d1e cb20ff86",
    "1d1fa7dd ad8979e7 4c97cbe5 947f8048 61d501d1 f02293fa 2a3f141c 31f7f1e8 fa905bff 53bc04e2 03fa93ac 5d9627f7",
    "1d1fa7dd afc978e7 4c97cbe5 946fc049 61d511d1 f02293fa 2a2f1c18 f17da9e9 056fbbfe 4698522a 4b6b3d6e 0e3d7f44",
    "1d1fafdd ada879e7 4c97cbe5 947b8048 61d121d3 7026b3fa aa2f2c19 3163b1ec 052fbbfa 48cb0f04 8724b9ce 40322cd4",
    "1d1fafdd afa87ae7 4c97cbe5 947f8048 61c171d1 7026b3fa 2a2f341d 31fbb9e8 052fbbfe 06d377f8 a72238b6 e6775d76",
    "1d1fafdd adaa79e7 4cd7cae5 947fc049 61c151d1 7026b3fa 2a371c1c f171e1e8 052fb3fe 6ad8c2a8 c32b9a64 6c798ede",
    "1d1fafdd adca78e7 4c97cbe5 943bc249 61d503d3 7026b3fa 2a27041c 717989e8 f99073fb 30a96c7c 09bbd53c da8e6087",
    "1d1fafdd afe979e7 4c97cbe5 947f8048 61d521d3 f02293fa aa372418 717591e8 f99073fb 52a5b866 4bff912c d294705f",
    "1d1fa7dd adea79e7 4c97cbe5 943bc249 61d563d1 f02293fa 2a3f3c19 f179f9e9 066f9bfe 0d9e46ea 056af9a6 0d7e8dfc",
    "1d1fa7dd afa97be7 4cd7cae5 946bc049 61c111d1 f02293fa 2a2f3c18 3167b1ec 052fb3fe 4ed812a0 6d2e5de4 242cbac4",
    "1d1fafdd afc978e7 4c97cbe5 946bc049 61c161d1 7026b3fa 2a273c1c 717191e9 fa9053ff bfbe0490 8dbc53dc 138e602f",
    "1d1fa7dd afa978e7 4cd7cae5 947b8048 61d141d1 7026b3fa aa3f3c1d 31eba1ed 052fbbfe cadc0632 036f1f7c 487c0eb6",
    "1d1fafdd afcb7ae7 4c97cbe5 946b8048 61c111d3 f02293fa 2a3f3c19 b16ba1ed 052fb3fa 20c0bf26 07671e64 a8659fbc",
    "1d1fafdd afcb7ae7 4c97cbe5 946b8048 61c111d3 f02293fa 2a3f3c19 b16ba1ed 052fb3fa 20c0bf26 07671e64 ea655fbc",
    "1d1fa7dd afea7ae7 4cd7cae5 947f8048 61c121d3 7026b3fa aa270418 f17df9e9 052fb3fa 048a8ac6 4569da0c a4718ea4",
    "1d1fa7dd adeb7ae7 4c97cbe5 947fc049 61d121d1 f02293fa aa3f0c18 f1f9e1e8 f99073ff b6b42120 4db35664 b8de0235",
]


def ror(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK


def S0(x):
    return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)


def S1(x):
    return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)


def s0(x):
    return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)


def s1(x):
    return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)


def IF(x, y, z):
    return (x & y) ^ (~x & MASK & z)


def MAJ(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def words(hexstr):
    b = bytes.fromhex(hexstr)
    return [int.from_bytes(b[4 * i:4 * i + 4], "big") for i in range(16)]


def compress(cv, m):
    w = list(m)
    for t in range(16, 31):
        w.append((s1(w[t - 2]) + w[t - 7] + s0(w[t - 15]) + w[t - 16]) & MASK)
    a, b, c, d, e, f, g, h = cv
    for t in range(31):
        t1 = (h + S1(e) + IF(e, f, g) + K[t] + w[t]) & MASK
        t2 = (S0(a) + MAJ(a, b, c)) & MASK
        a, b, c, d, e, f, g, h = (t1 + t2) & MASK, a, b, c, (d + t1) & MASK, e, f, g
    return [(x + y) & MASK for x, y in zip(cv, (a, b, c, d, e, f, g, h))]


def states(cv, w, last):
    """A_i, E_i for i = -4..last from chaining value cv and message words w."""
    A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}
    E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
    for i in range(last + 1):
        E[i] = (A[i - 4] + E[i - 4] + S1(E[i - 1]) + IF(E[i - 1], E[i - 2], E[i - 3]) + K[i] + w[i]) & MASK
        A[i] = (E[i] - A[i - 4] + S0(A[i - 1]) + MAJ(A[i - 1], A[i - 2], A[i - 3])) & MASK
    return A, E


class Stream:
    """Deterministic 32-bit words from the organizer trial seed (SHA-256 in counter mode)."""

    def __init__(self, seed_hex):
        self.seed = bytes.fromhex(seed_hex)
        self.ctr = 0
        self.buf = []

    def next(self):
        if not self.buf:
            h = hashlib.sha256(self.seed + self.ctr.to_bytes(8, "big")).digest()
            self.ctr += 1
            self.buf = [int.from_bytes(h[4 * i:4 * i + 4], "big") for i in range(8)]
        return self.buf.pop()


def trail_ok(A, E, Ap, Ep):
    for i in range(0, 13):
        ra, re = ROWS.get(i, ("=" * 32, "=" * 32))
        for x, xp, row in ((A[i], Ap[i], ra), (E[i], Ep[i], re)):
            d, v = signed(row)
            if (x ^ xp) != d or (x & d) != v:
                return False
    return True


def complete(m0, m1, rng, cap13=1 << 16, cap15=1 << 12):
    cv = compress(IV, m0)
    w = list(m1)
    wp = list(m1)
    for i in DW:
        wp[i] = (w[i] + DW[i]) & MASK
    A, E = states(cv, w, 12)
    Ap, Ep = states(cv, wp, 12)
    ok = trail_ok(A, E, Ap, Ep)
    w14 = w[14]
    w16 = (s1(w14) + w[9] + s0(w[1]) + w[0]) & MASK
    c13 = (A[9] + E[9] + S1(E[12]) + IF(E[12], E[11], E[10]) + K[13]) & MASK
    for t13 in range(1, cap13 + 1):
        e13 = rng.next()
        e14 = (A[10] + E[10] + S1(e13) + IF(e13, E[12], E[11]) + K[14] + w14) & MASK
        if (e14 & XE14) != VE14:
            continue
        e14p = (Ap[10] + Ep[10] + S1(e13) + IF(e13, Ep[12], Ep[11]) + K[14] + w14) & MASK
        if e14p != e14 ^ XE14:
            continue
        c15 = (A[11] + E[11] + S1(e14) + IF(e14, e13, E[12])) & MASK
        c15p = (Ap[11] + Ep[11] + S1(e14p) + IF(e14p, e13, Ep[12])) & MASK
        if c15 != c15p:
            continue
        for t15 in range(1, cap15 + 1):
            e15 = rng.next()
            e16 = (A[12] + E[12] + S1(e15) + IF(e15, e14, e13) + K[16] + w16) & MASK
            e16p = (Ap[12] + Ep[12] + S1(e15) + IF(e15, e14p, e13) + K[16] + w16 + DW16) & MASK
            if e16 != e16p or IF(e16, e15, e14) != IF(e16, e15, e14p):
                continue
            n1 = w[:13] + [(e13 - c13) & MASK, w14, (e15 - c15 - K[15]) & MASK]
            n1p = list(n1)
            for i in DW:
                n1p[i] = (n1[i] + DW[i]) & MASK
            if compress(cv, n1) != compress(cv, n1p):
                continue
            return n1, n1p, t13, t15, ok
        return None, None, t13, cap15, ok
    return None, None, cap13, 0, ok


def mdiff(row):
    d, v = signed(row)
    return ((v ^ d) - v) & MASK


def base_valid(b):
    """Steps 5..13 of A and 8..13 of E for both messages, as in proof.md Section 4 (P1, P2)."""
    E = {i: b[i - 5] for i in range(5, 13)}
    A = {i: b[8 + i - 5] for i in range(5, 9)}
    A[4] = (E[8] - A[8] + S0(A[7]) + MAJ(A[7], A[6], A[5])) & MASK
    A[3] = (E[7] - A[7] + S0(A[6]) + MAJ(A[6], A[5], A[4])) & MASK
    A[2] = (E[6] - A[6] + S0(A[5]) + MAJ(A[5], A[4], A[3])) & MASK
    A[1] = (E[5] - A[5] + S0(A[4]) + MAJ(A[4], A[3], A[2])) & MASK
    for i in range(9, 13):
        A[i] = (E[i] - A[i - 4] + S0(A[i - 1]) + MAJ(A[i - 1], A[i - 2], A[i - 3])) & MASK
    xa = {i: signed(ROWS.get(i, ("=" * 32, "=" * 32))[0]) for i in range(1, 13)}
    xe = {i: signed(ROWS.get(i, ("=" * 32, "=" * 32))[1]) for i in range(5, 13)}
    Ap = {i: A[i] ^ xa[i][0] for i in A}
    Ep = {i: E[i] ^ xe[i][0] for i in E}
    for i in range(1, 13):
        if (A[i] & xa[i][0]) != xa[i][1]:
            return False
    for i in range(5, 13):
        if (E[i] & xe[i][0]) != xe[i][1]:
            return False
        if Ap[i] != (Ep[i] - Ap[i - 4] + S0(Ap[i - 1]) + MAJ(Ap[i - 1], Ap[i - 2], Ap[i - 3])) & MASK:
            return False
    if MAJ(A[12], A[11], Ap[10]) != MAJ(A[12], A[11], A[10]):
        return False
    dw = {8: DW[8], 9: DW[9], 10: 0, 11: 0, 12: 0}
    for i in range(9, 13):
        w = (E[i] - A[i - 4] - E[i - 4] - S1(E[i - 1]) - IF(E[i - 1], E[i - 2], E[i - 3]) - K[i]) & MASK
        wp = (w + dw[i]) & MASK
        if Ep[i] != (Ap[i - 4] + Ep[i - 4] + S1(Ep[i - 1]) + IF(Ep[i - 1], Ep[i - 2], Ep[i - 3]) + K[i] + wp) & MASK:
            return False
    w8d = (mdiff(ROWS[8][1]) - (S1(Ep[7]) - S1(E[7])) - (IF(Ep[7], Ep[6], Ep[5]) - IF(E[7], E[6], E[5]))) & MASK
    if w8d != DW[8]:
        return False   # step 8 (E-only part)
    d13 = (mdiff(ROWS[9][1]) + (S1(Ep[12]) - S1(E[12])) + (IF(Ep[12], Ep[11], Ep[10]) - IF(E[12], E[11], E[10]))) & MASK
    if d13 != 0:
        return False   # step 13 (E-only part): no difference in E13
    w9 = (E[9] - A[5] - E[5] - S1(E[8]) - IF(E[8], E[7], E[6]) - K[9]) & MASK
    return ((s0((w9 + DW[9]) & MASK) - s0(w9)) & MASK) == ((-DW[8]) & MASK)


def to_hex(ws):
    return b"".join(x.to_bytes(4, "big") for x in ws).hex()


def main():
    req = json.loads(sys.stdin.read())
    nvalid = sum(base_valid([int(x, 16) for x in row.split()]) for row in BASES)
    out = []
    for t in req["trials"]:
        idx = t["trial"] % len(PAIRS)
        m0, m1 = words(PAIRS[idx][0]), words(PAIRS[idx][1])
        n1, n1p, t13, t15, ok = complete(m0, m1, Stream(t["seed"]))
        obs = {"pair_index": idx, "e13_draws": t13, "e15_draws": t15, "steps_0_12_follow_table6": ok,
               "advice_bases_valid": nvalid, "advice_bases": len(BASES)}
        if n1 is None:
            out.append({"trial": t["trial"], "message_a_hex": None, "message_b_hex": None, "observations": obs})
        else:
            out.append({"trial": t["trial"], "message_a_hex": to_hex(m0 + n1), "message_b_hex": to_hex(m0 + n1p),
                        "observations": obs})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": out}, separators=(",", ":")))


if __name__ == "__main__":
    main()
