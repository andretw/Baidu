# -*- coding: utf-8 -*-

locations =  {
  u"北京" : [ 
    u"东城", 
    u"西城", 
    u"崇文", 
    u"宣武", 
    u"朝阳", 
    u"海淀", 
    u"丰台", 
    u"石景山", 
    u"房山", 
    u"通州", 
    u"顺义", 
    u"昌平", 
    u"大兴", 
    u"怀柔", 
    u"平谷", 
    u"门头沟", 
    u"密云", 
    u"延庆", 
  ],
  u"广东" : [ 
    u"广州", 
    u"深圳", 
    u"珠海", 
    u"汕头", 
    u"韶关", 
    u"佛山", 
    u"江门", 
    u"湛江", 
    u"茂名", 
    u"肇庆", 
    u"惠州", 
    u"梅州", 
    u"汕尾", 
    u"河源", 
    u"阳江", 
    u"清远", 
    u"东莞", 
    u"中山", 
    u"潮州", 
    u"揭阳", 
    u"云浮", 
  ],
  u"上海" : [ 
    u"黄浦", 
    u"卢湾", 
    u"徐汇", 
    u"长宁", 
    u"静安", 
    u"普陀", 
    u"闸北", 
    u"虹口", 
    u"杨浦", 
    u"宝山", 
    u"闵行", 
    u"嘉定", 
    u"松江", 
    u"金山", 
    u"青浦", 
    u"南汇", 
    u"奉贤", 
    u"浦东新", 
    u"崇明", 
  ],
  u"天津" : [ 
    u"和平", 
    u"河东", 
    u"河西", 
    u"南开", 
    u"河北", 
    u"红桥", 
    u"塘沽", 
    u"汉沽", 
    u"大港", 
    u"东丽", 
    u"西青", 
    u"北辰", 
    u"津南", 
    u"武清", 
    u"宝坻", 
    u"静海", 
    u"宁河", 
    u"蓟", 
  ],
  u"重庆" : [ 
    u"渝中", 
    u"大渡口", 
    u"江北", 
    u"南岸", 
    u"北碚", 
    u"渝北", 
    u"巴南", 
    u"长寿", 
    u"双桥", 
    u"沙坪坝", 
    u"万盛", 
    u"万州", 
    u"涪陵", 
    u"黔江", 
    u"永川", 
    u"合川", 
    u"江津", 
    u"九龙坡", 
    u"南川", 
    u"綦江", 
    u"潼南", 
    u"荣昌", 
    u"璧山", 
    u"大足", 
    u"铜梁", 
    u"梁平", 
    u"开", 
    u"忠", 
    u"城口", 
    u"垫江", 
    u"武隆", 
    u"丰都", 
    u"奉节", 
    u"云阳", 
    u"巫溪", 
    u"巫山", 
    u"石柱土家族自治", 
    u"秀山土家族苗族自治", 
    u"酉阳土家族苗族自治", 
    u"彭水苗族土家族自治", 
  ],
  u"辽宁" : [ 
    u"沈阳", 
    u"大连", 
    u"鞍山", 
    u"抚顺", 
    u"本溪", 
    u"丹东", 
    u"锦州", 
    u"营口", 
    u"阜新", 
    u"辽阳", 
    u"盘锦", 
    u"铁岭", 
    u"朝阳", 
    u"葫芦岛", 
  ],
  u"江苏" : [ 
    u"南京", 
    u"苏州", 
    u"无锡", 
    u"常州", 
    u"镇江", 
    u"南通", 
    u"泰州", 
    u"扬州", 
    u"盐城", 
    u"连云港", 
    u"徐州", 
    u"淮安", 
    u"宿迁", 
  ],
  u"湖北" : [ 
    u"武汉", 
    u"黄石", 
    u"十堰", 
    u"荆州", 
    u"宜昌", 
    u"襄樊", 
    u"鄂州", 
    u"荆门", 
    u"孝感", 
    u"黄冈", 
    u"咸宁", 
    u"随州", 
    u"恩施土家族苗族自治州", 
    u"仙桃", 
    u"天门", 
    u"潜江", 
    u"神农架林", 
  ],
  u"四川" : [ 
    u"成都", 
    u"自贡", 
    u"攀枝花", 
    u"泸州", 
    u"德阳", 
    u"绵阳", 
    u"广元", 
    u"遂宁", 
    u"内江", 
    u"乐山", 
    u"南充", 
    u"眉山", 
    u"宜宾", 
    u"广安", 
    u"达州", 
    u"雅安", 
    u"巴中", 
    u"资阳", 
    u"阿坝藏族羌族自治州", 
    u"甘孜藏族自治州", 
    u"凉山彝族自治州", 
  ],
  u"陕西" : [ 
    u"西安", 
    u"铜川", 
    u"宝鸡", 
    u"咸阳", 
    u"渭南", 
    u"延安", 
    u"汉中", 
    u"榆林", 
    u"安康", 
    u"商洛", 
  ],
  u"河北" : [ 
    u"石家庄", 
    u"唐山", 
    u"秦皇岛", 
    u"邯郸", 
    u"邢台", 
    u"保定", 
    u"张家口", 
    u"承德", 
    u"沧州", 
    u"廊坊", 
    u"衡水", 
  ],
  u"山西" : [ 
    u"太原", 
    u"大同", 
    u"阳泉", 
    u"长治", 
    u"晋城", 
    u"朔州", 
    u"晋中", 
    u"运城", 
    u"忻州", 
    u"临汾", 
    u"吕梁", 
  ],
  u"河南" : [ 
    u"郑州", 
    u"开封", 
    u"洛阳", 
    u"平顶山", 
    u"安阳", 
    u"鹤壁", 
    u"新乡", 
    u"焦作", 
    u"濮阳", 
    u"许昌", 
    u"漯河", 
    u"三门峡", 
    u"南阳", 
    u"商丘", 
    u"信阳", 
    u"周口", 
    u"驻马店", 
    u"焦作", 
  ],
  u"吉林" : [ 
    u"长春", 
    u"吉林", 
    u"四平", 
    u"辽源", 
    u"通化", 
    u"白山", 
    u"松原", 
    u"白城", 
    u"延边朝鲜族自治州", 
  ],
  u"黑龙江" : [ 
    u"哈尔滨", 
    u"齐齐哈尔", 
    u"鹤岗", 
    u"双鸭山", 
    u"鸡西", 
    u"大庆", 
    u"伊春", 
    u"牡丹江", 
    u"佳木斯", 
    u"七台河", 
    u"黑河", 
    u"绥化", 
    u"大兴安岭地", 
  ],
  u"内蒙古" : [ 
    u"呼和浩特", 
    u"包头", 
    u"乌海", 
    u"赤峰", 
    u"通辽", 
    u"鄂尔多斯", 
    u"呼伦贝尔", 
    u"巴彦淖尔", 
    u"乌兰察布", 
    u"锡林郭勒盟", 
    u"兴安盟", 
    u"阿拉善盟", 
  ],
  u"山东" : [ 
    u"济南", 
    u"青岛", 
    u"淄博", 
    u"枣庄", 
    u"东营", 
    u"烟台", 
    u"潍坊", 
    u"济宁", 
    u"泰安", 
    u"威海", 
    u"日照", 
    u"莱芜", 
    u"临沂", 
    u"德州", 
    u"聊城", 
    u"滨州", 
    u"菏泽", 
  ],
  u"安徽" : [ 
    u"合肥", 
    u"芜湖", 
    u"蚌埠", 
    u"淮南", 
    u"马鞍山", 
    u"淮北", 
    u"铜陵", 
    u"安庆", 
    u"黄山", 
    u"滁州", 
    u"阜阳", 
    u"宿州", 
    u"巢湖", 
    u"六安", 
    u"亳州", 
    u"池州", 
    u"宣城", 
  ],
  u"浙江" : [ 
    u"杭州", 
    u"宁波", 
    u"温州", 
    u"嘉兴", 
    u"湖州", 
    u"绍兴", 
    u"金华", 
    u"衢州", 
    u"舟山", 
    u"台州", 
    u"丽水", 
  ],
  u"福建" : [ 
    u"福州", 
    u"厦门", 
    u"莆田", 
    u"三明", 
    u"泉州", 
    u"漳州", 
    u"南平", 
    u"龙岩", 
    u"宁德", 
  ],
  u"湖南" : [ 
    u"长沙", 
    u"株洲", 
    u"湘潭", 
    u"衡阳", 
    u"邵阳", 
    u"岳阳", 
    u"常德", 
    u"张家界", 
    u"益阳", 
    u"郴州", 
    u"永州", 
    u"怀化", 
    u"娄底", 
    u"湘西土家族苗族自治州", 
  ],
  u"广西" : [ 
    u"南宁", 
    u"柳州", 
    u"桂林", 
    u"梧州", 
    u"北海", 
    u"防城港", 
    u"钦州", 
    u"贵港", 
    u"玉林", 
    u"百色", 
    u"贺州", 
    u"河池", 
    u"来宾", 
    u"崇左", 
  ],
  u"江西" : [ 
    u"南昌", 
    u"景德镇", 
    u"萍乡", 
    u"九江", 
    u"新余", 
    u"鹰潭", 
    u"赣州", 
    u"吉安", 
    u"宜春", 
    u"抚州", 
    u"上饶", 
  ],
  u"贵州" : [ 
    u"贵阳", 
    u"六盘水", 
    u"遵义", 
    u"安顺", 
    u"铜仁地", 
    u"毕节地", 
    u"黔西南布依族苗族自治州", 
    u"黔东南苗族侗族自治州", 
    u"黔南布依族苗族自治州", 
  ],
  u"云南" : [ 
    u"昆明", 
    u"曲靖", 
    u"玉溪", 
    u"保山", 
    u"昭通", 
    u"丽江", 
    u"普洱", 
    u"临沧", 
    u"德宏傣族景颇族自治州", 
    u"怒江傈僳族自治州", 
    u"迪庆藏族自治州", 
    u"大理白族自治州", 
    u"楚雄彝族自治州", 
    u"红河哈尼族彝族自治州", 
    u"文山壮族苗族自治州", 
    u"西双版纳傣族自治州", 
  ],
  u"西藏" : [ 
    u"拉萨", 
    u"那曲地", 
    u"昌都地", 
    u"林芝地", 
    u"山南地", 
    u"日喀则地", 
    u"阿里地", 
  ],
  u"海南" : [ 
    u"海口", 
    u"三亚", 
    u"五指山", 
    u"琼海", 
    u"儋州", 
    u"文昌", 
    u"万宁", 
    u"东方", 
    u"澄迈", 
    u"定安", 
    u"屯昌", 
    u"临高", 
    u"白沙黎族自治", 
    u"昌江黎族自治", 
    u"乐东黎族自治", 
    u"陵水黎族自治", 
    u"保亭黎族苗族自治", 
    u"琼中黎族苗族自治", 
  ],
  u"甘肃" : [ 
    u"兰州", 
    u"嘉峪关", 
    u"金昌", 
    u"白银", 
    u"天水", 
    u"武威", 
    u"酒泉", 
    u"张掖", 
    u"庆阳", 
    u"平凉", 
    u"定西", 
    u"陇南", 
    u"临夏回族自治州", 
    u"甘南藏族自治州", 
  ],
  u"宁夏" : [ 
    u"银川", 
    u"石嘴山", 
    u"吴忠", 
    u"固原", 
    u"中卫", 
  ],
  u"青海" : [ 
    u"西宁", 
    u"海东地", 
    u"海北藏族自治州", 
    u"海南藏族自治州", 
    u"黄南藏族自治州", 
    u"果洛藏族自治州", 
    u"玉树藏族自治州", 
    u"海西蒙古族藏族自治州", 
  ],
  u"新疆" : [ 
    u"乌鲁木齐", 
    u"克拉玛依", 
    u"吐鲁番地", 
    u"哈密地", 
    u"和田地", 
    u"阿克苏地", 
    u"喀什地", 
    u"克孜勒苏柯尔克孜自治州", 
    u"巴音郭楞蒙古自治州", 
    u"昌吉回族自治州", 
    u"博尔塔拉蒙古自治州", 
    u"石河子", 
    u"阿拉尔", 
    u"图木舒克", 
    u"五家渠", 
    u"伊犁哈萨克自治州", 
  ],
  u"香港" : [ 
    u"中西", 
    u"湾仔", 
    u"东", 
    u"南", 
    u"深水埗", 
    u"油尖旺", 
    u"九龙城", 
    u"黄大仙", 
    u"观塘", 
    u"北", 
    u"大埔", 
    u"沙田", 
    u"西贡", 
    u"元朗", 
    u"屯门", 
    u"荃湾", 
    u"葵青", 
    u"离岛", 
  ],
  u"澳门" : [ 
    u"花地玛堂", 
    u"圣安多尼堂", 
    u"大堂", 
    u"望德堂", 
    u"风顺堂", 
    u"嘉模堂", 
    u"圣方济各堂", 
    u"路凼", 
  ]
}