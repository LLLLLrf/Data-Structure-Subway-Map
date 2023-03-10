from geopy.distance import geodesic
import Adjacent

'''
————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
以下为 生成以邻接表形式存储的图 和 将邻接表导出为pickle文件 使用的函数
'''

'''
用于生成graph的pkl文件
根据preData中的数据生成所有广州地铁站组成的邻接表
并将邻接表导出为pickle文件,保存于根目录下
'''


def get_graph():
    # 广州地铁数据
    preData = {
        'Adjacent.Station': ['广州东站', '体育中心', '体育西路', '杨箕', '东山口', '烈士陵园', '农讲所', '公园前',
                             '西门口', '陈家祠', '长寿路', '黄沙', '芳村', '花地湾', '坑口', '西塱', '广州南站', '石壁',
                             '会江', '南浦', '洛溪', '南洲', '东晓南', '江泰路', '昌岗', '江南西', '市二宫', '海珠广场',
                             '公园前', '纪念堂', '越秀公园', '广州火车站', '三元里', '飞翔公园', '白云公园',
                             '白云文化广场', '萧岗', '江夏', '黄边', '嘉禾望岗', '番禺广场', '市桥', '汉溪长隆', '大石',
                             '厦滘', '沥滘', '大塘', '客村', '广州塔', '珠江新城', '体育西路', '石牌桥', '岗顶', '华师',
                             '五山', '天河客运站', '机场北', '机场南', '高增', '人和', '龙归', '嘉禾望岗', '白云大道北',
                             '永泰', '同和', '京溪南方医院', '梅花园', '燕塘', '广州东站', '林和西', '体育西路',
                             '南沙客运港', '南横', '塘坑', '大涌', '广隆', '飞沙角', '金洲', '蕉门', '黄阁',
                             '黄阁汽车城',
                             '庆盛', '东涌', '低涌', '海傍', '石碁', '新造', '大学城南', '大学城北', '官洲', '万胜围',
                             '车陂南', '车陂', '黄村', '滘口', '坦尾', '中山八', '西场', '西村', '广州火车站', '小北',
                             '淘金', '区庄', '动物园', '杨箕', '五羊邨', '珠江新城', '猎德', '潭村', '员村', '科韵路',
                             '车陂南', '东圃', '三溪', '鱼珠', '大沙地', '大沙东', '文冲', '浔峰岗', '横沙', '沙贝',
                             '河沙', '坦尾', '如意坊', '黄沙', '文化公园', '一德路', '海珠广场', '北京路', '团一大广场',
                             '东湖', '东山口', '区庄', '黄花岗', '沙河顶', '天平架', '燕塘', '天河客运站', '长湴',
                             '植物园', '龙洞', '柯木塱', '高塘石', '黄陂', '金峰', '暹岗', '苏元', '萝岗', '香雪',
                             '美的大道', '北滘公园', '美的', '南涌', '锦龙', '陈村', '陈村北', '大洲', '广州南站',
                             '石壁',
                             '谢村', '钟村', '汉溪长隆', '南村万博', '员岗', '板桥', '大学城南', '万胜围', '琶洲',
                             '新港东', '磨碟沙', '赤岗', '客村', '鹭江', '中大', '晓港', '昌岗', '宝岗大道', '沙园',
                             '凤凰新村', '同福西', '文化公园', '华林寺', '陈家祠', '彩虹桥', '鹅掌坦', '同德', '上步',
                             '聚龙', '石潭', '小坪', '石井', '亭岗', '滘心', '飞鹅岭', '花都汽车城', '广州北站',
                             '花城路',
                             '花果山公园', '花都广场', '马鞍山公园', '莲塘', '清布', '清塘', '高增', '鱼珠', '裕丰围',
                             '双岗', '南海神庙', '夏园', '南岗', '沙村', '白江', '新塘', '官湖', '新沙', '嘉禾望岗',
                             '白云东平', '夏良', '太和', '竹料', '钟落潭', '马沥', '新和', '太平', '神岗', '邓村',
                             '从化客运站', '东风', '新和', '红卫', '新南', '枫下', '知识城', '何棠下', '旺村', '汤村',
                             '镇龙北', '镇龙', '冼村', '磨碟沙', '龙潭', '沙溪', '南村万博', '番禺广场', '横沥',
                             '万顷沙',
                             '员村', '天河公园', '棠东', '黄村', '大观南路', '天河智慧城', '神舟路', '科学城', '苏元',
                             '水西', '长平', '金坑', '镇龙西', '镇龙', '中新', '坑贝', '凤岗', '朱村', '山田', '钟岗',
                             '增城广场', '番禺广场', '市广路', '广州南站', '陈头岗', '林和西', '体育中心南', '天河南',
                             '黄埔大道', '妇儿中心', '花城大道', '大剧院', '海心沙', '广州塔', '新城东', '东平',
                             '世纪莲',
                             '澜石', '魁奇路', '季华园', '同济路', '祖庙', '普君北路', '朝安', '桂城', '南桂路', '礌岗',
                             '千灯湖', '金融高新区', '龙溪', '菊树', '西塱', '鹤洞', '沙涌', '沙园', '燕岗', '石溪',
                             '南洲', '沥滘'],
        'line': ['广州地铁1号线', '广州地铁1号线', '广州地铁1号线', '广州地铁1号线', '广州地铁1号线',
                 '广州地铁1号线', '广州地铁1号线', '广州地铁1号线', '广州地铁1号线', '广州地铁1号线',
                 '广州地铁1号线', '广州地铁1号线', '广州地铁1号线', '广州地铁1号线', '广州地铁1号线',
                 '广州地铁1号线', '广州地铁2号线', '广州地铁2号线', '广州地铁2号线', '广州地铁2号线',
                 '广州地铁2号线', '广州地铁2号线', '广州地铁2号线', '广州地铁2号线', '广州地铁2号线',
                 '广州地铁2号线', '广州地铁2号线', '广州地铁2号线', '广州地铁2号线', '广州地铁2号线',
                 '广州地铁2号线', '广州地铁2号线', '广州地铁2号线', '广州地铁2号线', '广州地铁2号线',
                 '广州地铁2号线', '广州地铁2号线', '广州地铁2号线', '广州地铁2号线', '广州地铁2号线',
                 '广州地铁3号线', '广州地铁3号线', '广州地铁3号线', '广州地铁3号线', '广州地铁3号线',
                 '广州地铁3号线', '广州地铁3号线', '广州地铁3号线', '广州地铁3号线', '广州地铁3号线',
                 '广州地铁3号线', '广州地铁3号线', '广州地铁3号线', '广州地铁3号线', '广州地铁3号线',
                 '广州地铁3号线', '广州地铁3号线北延段', '广州地铁3号线北延段', '广州地铁3号线北延段',
                 '广州地铁3号线北延段', '广州地铁3号线北延段', '广州地铁3号线北延段', '广州地铁3号线北延段',
                 '广州地铁3号线北延段', '广州地铁3号线北延段', '广州地铁3号线北延段', '广州地铁3号线北延段',
                 '广州地铁3号线北延段', '广州地铁3号线北延段', '广州地铁3号线北延段', '广州地铁3号线北延段',
                 '广州地铁4号线', '广州地铁4号线', '广州地铁4号线', '广州地铁4号线', '广州地铁4号线',
                 '广州地铁4号线', '广州地铁4号线', '广州地铁4号线', '广州地铁4号线', '广州地铁4号线',
                 '广州地铁4号线', '广州地铁4号线', '广州地铁4号线', '广州地铁4号线', '广州地铁4号线',
                 '广州地铁4号线', '广州地铁4号线', '广州地铁4号线', '广州地铁4号线', '广州地铁4号线',
                 '广州地铁4号线', '广州地铁4号线', '广州地铁4号线', '广州地铁5号线', '广州地铁5号线',
                 '广州地铁5号线', '广州地铁5号线', '广州地铁5号线', '广州地铁5号线', '广州地铁5号线',
                 '广州地铁5号线', '广州地铁5号线', '广州地铁5号线', '广州地铁5号线', '广州地铁5号线',
                 '广州地铁5号线', '广州地铁5号线', '广州地铁5号线', '广州地铁5号线', '广州地铁5号线',
                 '广州地铁5号线', '广州地铁5号线', '广州地铁5号线', '广州地铁5号线', '广州地铁5号线',
                 '广州地铁5号线', '广州地铁5号线', '广州地铁6号线', '广州地铁6号线', '广州地铁6号线',
                 '广州地铁6号线', '广州地铁6号线', '广州地铁6号线', '广州地铁6号线', '广州地铁6号线',
                 '广州地铁6号线', '广州地铁6号线', '广州地铁6号线', '广州地铁6号线', '广州地铁6号线',
                 '广州地铁6号线', '广州地铁6号线', '广州地铁6号线', '广州地铁6号线', '广州地铁6号线',
                 '广州地铁6号线', '广州地铁6号线', '广州地铁6号线', '广州地铁6号线', '广州地铁6号线',
                 '广州地铁6号线', '广州地铁6号线', '广州地铁6号线', '广州地铁6号线', '广州地铁6号线',
                 '广州地铁6号线', '广州地铁6号线', '广州地铁6号线', '广州地铁7号线', '广州地铁7号线',
                 '广州地铁7号线', '广州地铁7号线', '广州地铁7号线', '广州地铁7号线', '广州地铁7号线',
                 '广州地铁7号线', '广州地铁7号线', '广州地铁7号线', '广州地铁7号线', '广州地铁7号线',
                 '广州地铁7号线', '广州地铁7号线', '广州地铁7号线', '广州地铁7号线', '广州地铁7号线',
                 '广州地铁8号线', '广州地铁8号线', '广州地铁8号线', '广州地铁8号线', '广州地铁8号线',
                 '广州地铁8号线', '广州地铁8号线', '广州地铁8号线', '广州地铁8号线', '广州地铁8号线',
                 '广州地铁8号线', '广州地铁8号线', '广州地铁8号线', '广州地铁8号线', '广州地铁8号线',
                 '广州地铁8号线', '广州地铁8号线', '广州地铁8号线', '广州地铁8号线', '广州地铁8号线',
                 '广州地铁8号线', '广州地铁8号线', '广州地铁8号线', '广州地铁8号线', '广州地铁8号线',
                 '广州地铁8号线', '广州地铁8号线', '广州地铁9号线', '广州地铁9号线', '广州地铁9号线',
                 '广州地铁9号线', '广州地铁9号线', '广州地铁9号线', '广州地铁9号线', '广州地铁9号线',
                 '广州地铁9号线', '广州地铁9号线', '广州地铁9号线', '广州地铁13号线', '广州地铁13号线',
                 '广州地铁13号线', '广州地铁13号线', '广州地铁13号线', '广州地铁13号线', '广州地铁13号线',
                 '广州地铁13号线', '广州地铁13号线', '广州地铁13号线', '广州地铁13号线', '广州地铁14号线',
                 '广州地铁14号线', '广州地铁14号线', '广州地铁14号线', '广州地铁14号线', '广州地铁14号线',
                 '广州地铁14号线', '广州地铁14号线', '广州地铁14号线', '广州地铁14号线', '广州地铁14号线',
                 '广州地铁14号线', '广州地铁14号线', '广州地铁14号线支线(知识城线)',
                 '广州地铁14号线支线(知识城线)', '广州地铁14号线支线(知识城线)', '广州地铁14号线支线(知识城线)',
                 '广州地铁14号线支线(知识城线)', '广州地铁14号线支线(知识城线)', '广州地铁14号线支线(知识城线)',
                 '广州地铁14号线支线(知识城线)', '广州地铁14号线支线(知识城线)', '广州地铁14号线支线(知识城线)',
                 '广州地铁18号线', '广州地铁18号线', '广州地铁18号线', '广州地铁18号线', '广州地铁18号线',
                 '广州地铁18号线', '广州地铁18号线', '广州地铁18号线', '广州地铁21号线', '广州地铁21号线',
                 '广州地铁21号线', '广州地铁21号线', '广州地铁21号线', '广州地铁21号线', '广州地铁21号线',
                 '广州地铁21号线', '广州地铁21号线', '广州地铁21号线', '广州地铁21号线', '广州地铁21号线',
                 '广州地铁21号线', '广州地铁21号线', '广州地铁21号线', '广州地铁21号线', '广州地铁21号线',
                 '广州地铁21号线', '广州地铁21号线', '广州地铁21号线', '广州地铁21号线', '广州地铁22号线',
                 '广州地铁22号线', '广州地铁22号线', '广州地铁22号线', '广州地铁APM线', '广州地铁APM线',
                 '广州地铁APM线', '广州地铁APM线', '广州地铁APM线', '广州地铁APM线', '广州地铁APM线',
                 '广州地铁APM线', '广州地铁APM线', '广州广佛线', '广州广佛线', '广州广佛线', '广州广佛线',
                 '广州广佛线', '广州广佛线', '广州广佛线', '广州广佛线', '广州广佛线', '广州广佛线',
                 '广州广佛线',
                 '广州广佛线', '广州广佛线', '广州广佛线', '广州广佛线', '广州广佛线', '广州广佛线',
                 '广州广佛线',
                 '广州广佛线', '广州广佛线', '广州广佛线', '广州广佛线', '广州广佛线', '广州广佛线',
                 '广州广佛线'],
        'longitude': [113.329619, 113.334945, 113.328159, 113.314869, 113.301875, 113.29219, 113.281939,
                      113.270719, 113.262402, 113.253344, 113.248586, 113.246955, 113.24251, 113.240659,
                      113.23904, 113.23897, 113.27613, 113.284372, 113.292953, 113.299986, 113.305167,
                      113.304229,
                      113.30085, 113.287003, 113.283298, 113.28034, 113.276541, 113.2723, 113.270719, 113.269851,
                      113.267926, 113.262048, 113.263705, 113.270061, 113.277335, 113.282019, 113.28681,
                      113.289643, 113.29371, 113.295567, 113.391065, 113.368331, 113.336832, 113.328283,
                      113.327237, 113.325595, 113.328211, 113.327116, 113.329847, 113.327696, 113.328159,
                      113.3382, 113.346151, 113.351857, 113.358452, 113.35038, 113.311835, 113.30939, 113.301941,
                      113.302458, 113.30738, 113.295567, 113.305064, 113.31289, 113.332926, 113.332571,
                      113.326945, 113.333697, 113.329619, 113.330364, 113.328159, 113.617552, 113.600929,
                      114.199301, 113.958734, 113.547156, 113.547097, 113.545281, 113.534004, 113.525192,
                      113.516188, 113.497012, 113.478955, 113.491307, 113.481909, 113.471801, 113.422056,
                      113.406995, 113.391948, 113.383237, 113.3912, 113.396613, 113.401879, 113.413531,
                      113.215087, 113.224749, 113.239335, 113.244563, 113.248607, 113.262048, 113.282932,
                      113.293286, 113.303399, 113.313797, 113.314869, 113.320796, 113.327696, 113.338872,
                      113.352488, 113.370485, 113.383678, 113.396613, 113.40807, 113.422344, 113.438887,
                      113.45269, 113.464838, 113.475478, 113.208259, 113.213283, 113.217802, 113.224066,
                      113.224749, 113.23785, 113.246955, 113.255854, 113.263704, 113.2723, 113.276481,
                      113.284569,
                      113.295078, 113.301875, 113.303399, 113.30648, 113.313442, 113.327398, 113.333697,
                      113.35038, 113.355914, 113.372236, 113.384137, 113.402612, 113.416974, 113.439765,
                      113.457778, 113.466794, 113.474944, 113.487845, 113.507439, 113.214311, 113.218769,
                      113.233441, 113.244389, 113.247851, 113.243214, 113.251709, 113.264081, 113.27613,
                      113.284372, 113.30276, 113.323503, 113.336832, 113.35279, 113.372568, 113.394399,
                      113.406995, 113.3912, 113.373171, 113.3637, 113.349193, 113.341561, 113.327116, 113.314756,
                      113.299561, 113.288344, 113.283298, 113.276136, 113.267027, 113.262653, 113.258891,
                      113.255854, 113.253736, 113.253344, 113.251016, 113.24248, 113.24125, 113.242348,
                      113.245442, 113.247627, 113.249553, 113.238013, 113.226445, 113.223497, 113.161418,
                      113.186639, 113.208547, 113.219353, 113.224906, 113.229342, 113.237815, 113.251755,
                      113.257351, 113.26929, 113.301941, 113.438887, 113.461869, 113.481065, 113.50396,
                      113.524588, 113.548146, 113.576873, 113.602151, 113.611796, 113.643074, 113.655759,
                      113.295567, 113.324347, 113.330187, 113.353659, 113.374908, 113.407386, 113.456937,
                      113.473605, 113.49851, 113.524023, 113.562947, 113.600864, 113.607151, 113.473605,
                      113.493683, 113.50165, 113.514754, 113.531558, 113.550265, 113.558158, 113.571129,
                      113.583669, 113.599635, 113.332889, 113.349193, 113.347796, 113.344847, 113.35279,
                      113.391065, 113.517805, 113.563762, 113.370485, 113.369203, 113.396419, 113.413531,
                      113.413212, 113.409787, 113.438259, 113.456426, 113.474944, 113.485758, 113.496375,
                      113.533321, 113.580266, 113.599635, 113.619602, 113.64939, 113.676978, 113.708077,
                      113.751097, 113.798663, 113.820912, 113.391065, 113.343804, 113.27613, 113.280658,
                      113.330364, 113.33019, 113.330694, 113.330916, 113.331216, 113.331292, 113.331248,
                      113.330888, 113.329847, 113.146407, 113.135677, 113.121016, 113.113758, 113.114854,
                      113.115088, 113.114935, 113.118754, 113.12929, 113.13968, 113.147803, 113.160495,
                      113.162422, 113.161978, 113.164135, 113.199177, 113.21941, 113.23897, 113.246665,
                      113.253377, 113.267027, 113.278408, 113.29253, 113.304229, 113.325595],
        'latitude': [23.156647, 23.140502, 23.136915, 23.133497, 23.13051, 23.132932, 23.132959, 23.131479,
                     23.131304, 23.131601, 23.124097, 23.115728, 23.104235, 23.09285, 23.084633, 23.071774,
                     22.995081, 23.000275, 23.019116, 23.040016, 23.049314, 23.070465, 23.077434, 23.088395,
                     23.096949, 23.103578, 23.112378, 23.121205, 23.131479, 23.138591, 23.145891, 23.153768,
                     23.165353, 23.175097, 23.18798, 23.196198, 23.204681, 23.217573, 23.228138, 23.243642,
                     22.940882, 22.955332, 22.999304, 23.023549, 23.043675, 23.060691, 23.083678, 23.102117,
                     23.112201, 23.125224, 23.136915, 23.13898, 23.14054, 23.146269, 23.158306, 23.176465,
                     23.402085, 23.392343, 23.361318, 23.341556, 23.294976, 23.243642, 23.228398, 23.226309,
                     23.202723, 23.190986, 23.181273, 23.165843, 23.156647, 23.147156, 23.136915, 22.773031,
                     22.753549, 22.644976, 22.548572, 22.778433, 22.788136, 22.79837, 22.806853, 22.830976,
                     22.842134, 22.872712, 22.885577, 22.925383, 22.945208, 22.962953, 23.034558, 23.049737,
                     23.064501, 23.073089, 23.103967, 23.121955, 23.130747, 23.139567, 23.119613, 23.131109,
                     23.13185, 23.143117, 23.147471, 23.153768, 23.145765, 23.142712, 23.140406, 23.140635,
                     23.133497, 23.12577, 23.125224, 23.12434, 23.123143, 23.12156, 23.125143, 23.121955,
                     23.115747, 23.110319, 23.106087, 23.109165, 23.111949, 23.109446, 23.170073, 23.163895,
                     23.158151, 23.140817, 23.131109, 23.12055, 23.115728, 23.114602, 23.119089, 23.121205,
                     23.124931, 23.124252, 23.121564, 23.13051, 23.140406, 23.147513, 23.153137, 23.165416,
                     23.165843, 23.176465, 23.184202, 23.196087, 23.197043, 23.199637, 23.197168, 23.194313,
                     23.186917, 23.177972, 23.176182, 23.181218, 23.178664, 22.950472, 22.935453, 22.93923,
                     22.945034, 22.95878, 22.9743, 22.982022, 22.990027, 22.995081, 23.000275, 22.996764,
                     22.992278, 22.999304, 23.009957, 23.021922, 23.023025, 23.049737, 23.103967, 23.104508,
                     23.104483, 23.105116, 23.10211, 23.102117, 23.101371, 23.09831, 23.099352, 23.096949,
                     23.092282, 23.094813, 23.100542, 23.10773, 23.114602, 23.124125, 23.131601, 23.137449,
                     23.162117, 23.169495, 23.176806, 23.187393, 23.193835, 23.206604, 23.216997, 23.228428,
                     23.24278, 23.384468, 23.386049, 23.382068, 23.385314, 23.393124, 23.40691, 23.399741,
                     23.39498, 23.384174, 23.378378, 23.361318, 23.106087, 23.100147, 23.100085, 23.089917,
                     23.089392, 23.101655, 23.116265, 23.129209, 23.138044, 23.143673, 23.143122, 23.243642,
                     23.256795, 23.28358, 23.304631, 23.354647, 23.382315, 23.399581, 23.419085, 23.458453,
                     23.481509, 23.501389, 23.537239, 23.572395, 23.419085, 23.405327, 23.383328, 23.369201,
                     23.355627, 23.337384, 23.329449, 23.313211, 23.295345, 23.29025, 23.128164, 23.105116,
                     23.086696, 23.041075, 23.009957, 22.940882, 22.759024, 22.704268, 23.12156, 23.13075,
                     23.137093, 23.139567, 23.150739, 23.169383, 23.171369, 23.171838, 23.176182, 23.192227,
                     23.216323, 23.255706, 23.283771, 23.29025, 23.291463, 23.285148, 23.281995, 23.278018,
                     23.282651, 23.28523, 23.283721, 22.940882, 22.97685, 22.995081, 23.025537, 23.147156,
                     23.139831, 23.137095, 23.132683, 23.128274, 23.124952, 23.121341, 23.117287, 23.112201,
                     22.964908, 22.971287, 22.970946, 22.989978, 22.999452, 23.012841, 23.024725, 23.032795,
                     23.033513, 23.033672, 23.037744, 23.040302, 23.048885, 23.061348, 23.072794, 23.071892,
                     23.071556, 23.071774, 23.078365, 23.089032, 23.094813, 23.081538, 23.074206, 23.070465,
                     23.060691]}
    graph = {}
    # 遍历广州地铁站以生成图的邻接表
    for i in range(len(preData['Adjacent.Station'])):
        # 若字典中不存在当前键，则增加格式为(站点名:站点对象)的键值对;若存在，则将对应的地铁线路添加到站点对象的line属性的列表中
        if graph.get(preData['Adjacent.Station'][i], None) is None:
            graph[preData['Adjacent.Station'][i]] = Adjacent.Station(preData['Adjacent.Station'][i])
        graph[preData['Adjacent.Station'][i]].line.append(preData['line'][i])
        # 判断当前站点是否与下一个站点属于同一条地铁线,若属于则互相将站点以格式为(站点名:站点距离)的键值对添加到邻接表字典中
        if i != len(preData['Adjacent.Station']) - 1 and preData['line'][i] == preData['line'][i + 1]:
            stationDistance = geodesic((float(preData['latitude'][i]), float(preData['longitude'][i])),
                                       (float(preData['latitude'][i + 1]), float(preData['longitude'][i + 1]))).m
            graph[preData['Adjacent.Station'][i]].subgraph[preData['Adjacent.Station'][i + 1]] = stationDistance
            if graph.get(preData['Adjacent.Station'][i + 1], None) is None:
                graph[preData['Adjacent.Station'][i + 1]] = Adjacent.Station(preData['Adjacent.Station'][i + 1])
            graph[preData['Adjacent.Station'][i + 1]].subgraph[preData['Adjacent.Station'][i]] = stationDistance
    return graph
