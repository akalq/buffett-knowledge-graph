#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复1996年巴菲特致股东信的中文翻译质量
使用格隆汇的完整翻译来补全不完整的翻译
"""

import re
from pathlib import Path

# 使用绝对路径
BASE_DIR = Path("/app/data/所有对话/主对话")
html_path = BASE_DIR / "投资研究/知识库/巴菲特知识库-LearnBuffett版/letters/berkshire/1996.html"
output_path = BASE_DIR / "投资研究/知识库/巴菲特知识库-LearnBuffett版/letters/berkshire/1996_fixed.html"

html_content = html_path.read_text(encoding='utf-8')

# 格隆汇完整翻译 - 按段落顺序排列
# 这是1996年巴菲特致股东信的完整中文翻译
REFERENCE_TRANSLATIONS = [
    # 0: 空块
    ("", ""),
    
    # 1: 致股东
    ("To the Shareholders of Berkshire Hathaway Inc.:", 
     "致伯克希尔·哈撒韦公司的全体股东："),
    
    # 2: 净值增长
    ("Our gain in net worth during 1996 was $6.2 billion, or 36.1%. Per- share book value, however, grew by less, 31.8%, because the number of  Berkshire shares increased: We issued stock in acquiring FlightSafety  International and also sold new Class B shares.* Over the last 32 years  (that is, since present management took over) per-share book value has  grown from $19 to $19,011, or at a rate of 23.8% compounded annually.",
     "1996年本公司的净值成长了36.1%，约62亿美元，不过每股净值仅成长了31.8%，原因在于去年我们以发行新股的方式并购了国际飞安公司，同时另外还追加发行了一些B级普通股，总计过去32年以来，也就是自从现有经营阶层接手之后，每股净值由当初的19元成长到现在的19,011美元，年复合成长率约为23.8%。"),
    
    # 3: B级股说明
    ("* Each Class B share has an economic interest equal to 1/30th of   that possessed by a Class A share, which is the new designation for   the only stock that Berkshire had outstanding before May 1996.   Throughout this report, we state all per-share figures in terms of  \"Class A equivalents,\" which are the sum of the Class A shares   outstanding and 1/30th of the Class B shares outstanding.",
     "（B级普通股拥有A级普通股三十分之一的权利，这是从1996年五月开始伯克希尔新增的股份类型，在年报中所谓的每股数字系以A级普通股约当数为基础，亦即全部流通在外的A级普通股数加上流通在外的B级普通股数的三十分之一。）"),
    
    # 4: 财务报表
    ("For technical reasons, we have restated our 1995 financial  statements, a matter that requires me to present one of my less-than- thrilling explanations of accounting arcana. I'll make it brief.",
     "基于技术性原因，我们必须将1995年的财务报表予以重编，这使我能够再度展现令人震惊的会计技巧，相信我，我会试着长话短说。"),
    
    # 5: GEICO并购
    ("The restatement was required because GEICO became a wholly-owned  subsidiary of Berkshire on January 2, 1996, whereas it was previously  classified as an investment. From an economic viewpoint - taking into  account major tax efficiencies and other benefits we gained - the value  of the 51% of GEICO we owned at year-end 1995 increased significantly  when we acquired the remaining 49% of the company two days later.  Accounting rules applicable to this type of \"step acquisition,\" however,  required us to write down the value of our 51% at the time we moved to  100%. That writedown - which also, of course, reduced book value -  amounted to $478.4 million. As a result, we now carry our original 51%  of GEICO at a value that is both lower than its market value at the time  we purchased the remaining 49% of the company and lower than the value at  which we carry that 49% itself.",
     "重编的原因是因为原先被列为被投资的盖可保险在1996年1月2日正式成为伯克希尔100%持有的子公司，从经济观点来看，考量可观的租税优惠与其它优点，我们原先在1995年底持有的51%的GEICO股权，其价值在二天后我们取得剩余49%股权之后大幅增加，然而对于这种渐进式购并，一般公认会计原则却要求我们必须在取得100%股权时，将原来账上51%的成本反向予以调减，使得账面价值减少为4.784亿美元，这结果使得原来51%股权的账面价值不但远低于后来49%股权的取得市价，也低于我们持有后来这49%股权的账面价值。"),
    
    # 6: 溢价发行
    ("There is an offset, however, to the reduction in book value I have  just described: Twice during 1996 we issued Berkshire shares at a  premium to book value, first in May when we sold the B shares for cash  and again in December when we used both A and B shares as part-payment  for FlightSafety. In total, the three non-operational items affecting  book value contributed less than one percentage point to our 31.8% per- share gain last year.",
     "不过除了刚刚提到净值的减少之外，我们在1996年两度溢价发行股份，第一次是在五月办理现金增资发行B级普通股，第二次是在十二月发行A级与B级普通股，以购并国际飞安公司，总的来说，以上三项非营业项目对于去年本公司31.8%的每股净值成长率的净影响还不到1%。"),
    
    # 7: 账面价值
    ("I dwell on this rise in per-share book value because it roughly  indicates our economic progress during the year. But, as Charlie Munger,  Berkshire's Vice Chairman, and I have repeatedly told you, what counts at  Berkshire is intrinsic value, not book value. The last time you got that  message from us was in the Owner's Manual, sent to you in June after we  issued the Class B shares. In that manual, we not only defined certain  key terms - such as intrinsic value - but also set forth our economic  principles.",
     "今年我之所以一再强调每股净值，原因在于它大约就等于我们在去年的实质进展，不过就像是查理跟我一再提醒各位的，对伯克希尔来说，真正重要的不是账面价值，而是实质价值，最近一次跟各位提到是在今年六月本公司发行B级普通股时，在送给各位的股东手册当中，我们不但对于一些名词予以定义，诸如实质价值等，同时也揭露了我们的企业宗旨。"),
    
    # 8: 股东手册
    ("For many years, we have listed these principles in the front of our  annual report, but in this report, on pages 58 to 67, we reproduce the  entire Owner's Manual. In this letter, we will occasionally refer to the  manual so that we can avoid repeating certain definitions and  explanations. For example, if you wish to brush up on \"intrinsic value,\"  see pages 64 and 65.",
     "多年来，我们在年报前头揭示这些宗旨，在这里我们偶尔也会提到股东手册，这样我们就可以不必再重复解释一些常用的名词，比如说如果你想要了解一下什么叫实质价值，建议大家可以再翻翻那本手册的第64、65页。"),
    
    # 9: 表格说明
    ("Last year, for the first time, we supplied you with a table that  Charlie and I believe will help anyone trying to estimate Berkshire's  intrinsic value. In the updated version of that table, which follows, we  trace two key indices of value. The first column lists our per-share  ownership of investments (including cash and equivalents) and the second  column shows our per-share earnings from Berkshire's operating businesses  before taxes and purchase-accounting adjustments but after all interest  and corporate overhead expenses. The operating-earnings column excludes all dividends, interest and capital gains that we realized from the  investments presented in the first column. In effect, the two columns  show what Berkshire would have reported had it been broken into two parts.",
     "从去年开始我们首度提供给各位一张查理跟我本人认为可以帮助大家估计伯克希尔公司实质价值的表格，在下面这张经过更新资料的表上，我们可以发现到两项与价值相关的重要指针，第一栏是我们平均每股持有的投资金额(包含现金与约当现金)，第二栏则是每股在扣除利息与营业费用之后，来自本业的营业利益(但未扣除所得税与购买法会计调整数)，当然后者已经扣除了所有来自第一栏投资所贡献的股利收入、利息收入与资本利得，事实上，若是把伯克希尔拆成两部分的话，这两栏数字将分别代表这两个部门的损益绩效。"),
    
    # 10: 表格数据
    ("\t\t Pre-tax Earnings Per Share \t Investments Excluding All Income from Year\t Per Share Investments  ---- ----------- ------------------------- 1965................................$ 4\t $ 4.08 1975................................\t 159\t (6.48) 1985................................\t2,443\t 18.86 1995................................ 22,088\t 258.20 1996................................ 28,500\t 421.39",
     ""),  # 表格数据，不需要翻译
    
    # 11: 表格解读
    ("As the table tells you, our investments per share increased in 1996  by 29.0% and our non-investment earnings grew by 63.2%. Our goal is to  keep the numbers in both columns moving ahead at a reasonable (or, better  yet, unreasonable) pace.",
     "从这张表大家可以看出，我们1996年的每股投资金额增加了29%，而非投资的本业盈余则增加了63.2%，我们的目标是让这两栏的数字以合理的速度稳定地成长，当然若是偶尔能以不合理的速度暴增也不错。"),
    
    # 12: 现实因素
    ("Our expectations, however, are tempered by two realities. First,  our past rates of growth cannot be matched nor even approached:  Berkshire's equity capital is now large - in fact, fewer than ten  businesses in America have capital larger - and an abundance of funds  tends to dampen returns. Second, whatever our rate of progress, it will  not be smooth: Year-to-year moves in the first column of the table above  will be influenced in a major way by fluctuations in securities markets;  the figures in the second column will be affected by wide swings in the  profitability of our catastrophe-reinsurance business.",
     "不过这样的预期可能会受到两项现实的因素所干扰，首先，我们很难再达到或接近过去那样高的成长速度，原因在于伯克希尔现在的资本规模实在是太庞大了，事实上以我们现在的资本规模已经可以排在全美企业的前十名，过多的资金一定会影响到整体的报酬率，第二点，不管成长的速度如何，铁定很难以平稳的速度增加，第一栏的数字将很容易随着股市大环境上下波动，第二栏的数字则会跟着超级灾害再保业务获利的不稳定变动而变化。"),
    
    # 13: 捐赠与开支
    ("In the table, the donations made pursuant to our shareholder- designated contributions program are charged against the second column,  though we view them as a shareholder benefit rather than as an expense.  All other corporate expenses are also charged against the second column.  These costs may be lower than those of any other large American  corporation: Our after-tax headquarters expense amounts to less than two  basis points (1/50th of 1%) measured against net worth. Even so, Charlie  used to think this expense percentage outrageously high, blaming it on my  use of Berkshire's corporate jet, The Indefensible. But Charlie has  recently experienced a \"counter-revelation\": With our purchase of  FlightSafety, whose major activity is the training of corporate pilots,  he now rhapsodizes at the mere mention of jets.",
     "在这张表中，股东指定捐赠的款项被列为第二栏的减项，虽然我们将之视为股东的福利而非支出，企业其它的支出同样也被放在第二栏当作减项，这些开支远低于其它美国大企业的平均水准，每年我们企业总部的费用占净值的比率大约不到万分之五，即便如此查理还是认为这样的比率高得离谱，我想主要要怪罪于我个人所使用的伯克希尔企业专机-无可辩解号，不过最近在我们买下国际飞安-这家专门负责训练飞行的公司之后，查理的态度有了180度的转变，现在只要一提到飞机他就狂乐不已。"),
    
    # 14: 成本控制
    ("Seriously, costs matter. For example, equity mutual funds incur  corporate expenses - largely payments to the funds' managers - that  average about 100 basis points, a levy likely to cut the returns their  investors earn by 10% or more over time. Charlie and I make no promises  about Berkshire's results. We do promise you, however, that virtually  all of the gains Berkshire makes will end up with shareholders. We are  here to make money with you, not off you.",
     "认真的说，控制成本开支绝对重要，举例来说很多共同基金每年的营业费用大多在2%上下，这等于间接剥削了投资人将近10%的投资报酬，虽然查理跟我不敢向各位保证我们的投资绩效，但我们却可以向各位打包票，伯克希尔所赚的每一分钱一定会分文不差地落入股东的口袋里，我们是来帮各位赚钱，而不是帮各位花钱的。"),
    
    # 15: 内在价值标题
    ("The Relationship of Intrinsic Value to Market Price",
     "实质价值与股票市价的关系"),
    
    # 16: 内在价值说明
    ("In last year's letter, with Berkshire shares selling at $36,000, I  told you: (1) Berkshire's gain in market value in recent years had  outstripped its gain in intrinsic value, even though the latter gain had  been highly satisfactory; (2) that kind of overperformance could not  continue indefinitely; (3) Charlie and I did not at that moment consider  Berkshire to be undervalued.",
     "去年当伯克希尔的股价约在36,000美元时，我曾向各位报告过(1)伯克希尔这几年的股价表现远超越实质价值，虽然后者的成长幅度也相当令人满意，(2)这样的情况不可能无限制地持续下去，(3)查理跟我不认为当时伯克希尔的价值有被低估的可能性。"),
    
    # 17: 内在价值变化
    ("Since I set down those cautions, Berkshire's intrinsic value has  increased very significantly - aided in a major way by a stunning  performance at GEICO that I will tell you more about later - while the  market price of our shares has changed little. This, of course, means  that in 1996 Berkshire's stock underperformed the business.  Consequently, today's price/value relationship is both much different  from what it was a year ago and, as Charlie and I see it, more  appropriate.",
     "自从我下了这些批注之后，伯克希尔的实质价值又大幅地增加了，主要的原因在于盖可惊人的表现(关于这点在后面还会向大家详细报告)，而在此同时伯克希尔的股价却维持不动，这代表在1996年伯克希尔的实质价值表现优于股价，也就是说，在今日伯克希尔的价格/价值比比起一年以前而言，又有很大的不同，这同时也是查理跟我认为比较合理的情况。"),
    
    # 18: 长期收益
    ("Over time, the aggregate gains made by Berkshire shareholders must  of necessity match the business gains of the company. When the stock  temporarily overperforms or underperforms the business, a limited number  of shareholders - either sellers or buyers - receive outsized benefits at  the expense of those they trade with. Generally, the sophisticated have  an edge over the innocents in this game.",
     "就长期而言，伯克希尔股东的整体利得一定会与企业经营的获利一致，当公司股价的表现暂时优于或劣于企业经营时，少部分的股东-不管是买进的人或是卖出的人，将会因为做出这样的举动而从交易的对方身上占到一些便宜，通常来说，都是老经验的一方在这场游戏中占上风。"),
    
    # 19: 股东利益
    ("Though our primary goal is to maximize the amount that our  shareholders, in total, reap from their ownership of Berkshire, we wish  also to minimize the benefits going to some shareholders at the expense  of others. These are goals we would have were we managing a family  partnership, and we believe they make equal sense for the manager of a  public company. In a partnership, fairness requires that partnership  interests be valued equitably when partners enter or exit; in a public  company, fairness prevails when market price and intrinsic value are in  sync. Obviously, they won't always meet that ideal, but a manager - by  his policies and communications - can do much to foster equity.",
     "虽然我们主要的目标是希望让伯克希尔的股东经由持有公司所有权所获得的利益极大化，但在此同时我们也期望能让一些股东从其它股东身上所占到的便宜能够极小化，我想这是一般人在经营家族企业时相当重视的，不过我们相信这也适用在上市公司的经营之上，对合伙企业来说，合伙权益在合伙人加入或退出时必须能够以合理的方式评量，才能维持公平，同样地，对于上市公司来说，惟有让公司的股价与实质价值一致，公司股东的公平性才得以维持，当然很明显，这样理想的情况很难一直维持，不过身为公司经理人可以透过其政策与沟通的方式来大力维持这样的公平性。"),
    
    # 20: 长期股东
    ("Of course, the longer a shareholder holds his shares, the more  bearing Berkshire's business results will have on his financial  experience - and the less it will matter what premium or discount to  intrinsic value prevails when he buys and sells his stock. That's one  reason we hope to attract owners with long-term horizons. Overall, I  think we have succeeded in that pursuit. Berkshire probably ranks number  one among large American corporations in the percentage of its shares  held by owners with a long-term view.",
     "当然股东持有股份的时间越长，那么伯克希尔本身的表现与他的投资经验就会越接近，而他买进或卖出股份时的价格相较于实质价值是折价或溢价的影响程度也就越小，这也是为什么我们希望能够吸引具有长期投资意愿的股东加入的原因之一，总的来说，我认为就这点而言，我们算是做的相当成功，伯克希尔大概是所有美国大企业中拥有最多具长期投资观点股东的公司。"),
    
    # 21: 并购标题
    ("Acquisitions of 1996",
     "1996年的并购案"),
    
    # 22: 并购概述
    ("We made two acquisitions in 1996, both possessing exactly the  qualities we seek - excellent business economics and an outstanding  manager.",
     "我们在1996年进行了两件并购案，两者皆拥有我们想要的特质-那就是绝佳的竞争优势与优秀的经理人。"),
    
    # 23: KBS收购
    ("The first acquisition was Kansas Bankers Surety (KBS), an insurance  company whose name describes its specialty. The company, which does  business in 22 states, has an extraordinary underwriting record, achieved  through the efforts of Don Towle, an extraordinary manager. Don has  developed first-hand relationships with hundreds of bankers and knows  every detail of his operation. He thinks of himself as running a company  that is \"his,\" an attitude we treasure at Berkshire. Because of its  relatively small size, we placed KBS with Wesco, our 80%-owned  subsidiary, which has wanted to expand its insurance operations.",
     "第一桩购并案是堪萨斯银行家保险-从字面上可知，这是一家专门提供银行业者保险的保险公司，在全美22个州从事相关业务，拥有相当不错的承保记录，全仰赖Don Towle这位杰出的经理人的努力，Don与上百位银行家皆保持良好的关系，而且也了解他所从事业务的每一项细节，那种感觉就好象是在经营\"自己\"的事业一样，这种精神是伯克希尔最欣赏的，由于它的规模不太大，同时正好伯克希尔持有80%股权的Wesco有意拓展保险事业，所以我们决定把它摆在Wesco之下成为其子公司。"),
    
    # 24: 生日宴会
    ("You might be interested in the carefully-crafted and sophisticated  acquisition strategy that allowed Berkshire to nab this deal. Early in  1996 I was invited to the 40th birthday party of my nephew's wife, Jane  Rogers. My taste for social events being low, I immediately, and in my  standard, gracious way, began to invent reasons for skipping the event.  The party planners then countered brilliantly by offering me a seat next  to a man I always enjoy, Jane's dad, Roy Dinsdale - so I went.",
     "大家或许会对我们这次精心设计的购并计划感到兴趣，在1996年初我受邀参加侄媳妇Jane40岁的生日宴会，由于我个人对于社交活动通常不太感兴趣，所以很自然地我按照惯例想出许多理由以婉拒这项邀请，不过对方显然有备而来，特别将我安排在另外一位我极有兴趣打交道的对象-Roy Dinsdale（Jane的父亲）的旁边，此举使得我无法拒绝而欣然赴会。"),
    
    # 25: 宴会交谈
    ("The party took place on January 26. Though the music was loud - Why  must bands play as if they will be paid by the decibel? - I just managed  to hear Roy say he'd come from a directors meeting at Kansas Bankers  Surety, a company I'd always admired. I shouted back that he should let  me know if it ever became available for purchase.",
     "生日宴会在1月26日举行，虽然当时现场音乐震耳欲聋(我实在搞不懂为何乐队总是要弹得那么大声，难道他们的出场费是按照分贝数计算的吗?)，不过我还是听到Roy说他刚参加完堪萨斯银行家保险的董事会，这是我一直相当欣赏的一家公司，我大声地响应他说，如果这家公司有意出售的话，记得一定要通知我。"),
    
    # 26: 来信和成交
    ("On February 12, I got the following letter from Roy: \"Dear Warren:  Enclosed is the annual financial information on Kansas Bankers Surety.  This is the company that we talked about at Janie's party. If I can be  of any further help, please let me know.\" On February 13, I told Roy we  would pay $75 million for the company - and before long we had a deal.  I'm now scheming to get invited to Jane's next party.",
     "2月12日我收到一封Roy的来函，上面写到：亲爱的沃伦，随函附送一份堪萨斯银行家保险的年度财务报表，就是上次在Jane的生日宴会上提到的那一家公司，如果你有任何需要，请务必让我知道。2月13日，我告诉Roy愿意出7,500万美元买下这家公司，不久之后，整个交易就搞定，现在的我正盘算明年还要再参加Jane的生日宴会。"),
    
    # 27: 飞安国际
    ("Our other acquisition in 1996 - FlightSafety International, the  world's leader in the training of pilots - was far larger, at about $1.5  billion, but had an equally serendipitous origin. The heroes of this  story are first, Richard Sercer, a Tucson aviation consultant, and  second, his wife, Alma Murphy, an ophthalmology graduate of Harvard  Medical School, who in 1990 wore down her husband's reluctance and got  him to buy Berkshire stock. Since then, the two have attended all our  Annual Meetings, but I didn't get to know them personally.",
     "1996年发生的另一件购并案，全世界最大的飞行员训练公司-国际飞安公司，其规模比起前一个案子要大得多了，总金额高达15亿美元，不过这个案子发生的过程一样充满戏剧性，本案的功臣首推Richard Sercer-他是塔克森市的飞行顾问，当然还要归功于他的妻子-Alma Murphy，哈佛医学院眼科学系毕业的她好不容易在1990年说服她的丈夫买进伯克希尔的股份，而且在那之后每年都到奥玛哈参加我们的股东会，只是我一直没有机会与他们认识。"),
    
    # 28: 牵线搭桥
    ("Fortunately, Richard had also been a long-time shareholder of  FlightSafety, and it occurred to him last year that the two companies  would make a good fit. He knew our acquisition criteria, and he thought  that Al Ueltschi, FlightSafety's 79-year-old CEO, might want to make a  deal that would both give him a home for his company and a security in  payment that he would feel comfortable owning throughout his lifetime.  So in July, Richard wrote Bob Denham, CEO of Salomon Inc, suggesting that  he explore the possibility of a merger.",
     "碰巧的是，Richard同时也是国际飞安公司长期投资的股东，刚好在去年他认为这两家公司应该有机会可以做一个结合，他相当了解伯克希尔购并公司的标准，同时也知道国际飞安79岁的总裁-Al Ueltschi想要为自己的公司找一个理想的归宿，好为自己的股权找到一层保障，所以就在七月份，Richard写信给所罗门公司的总裁-Bob Denham请他研究这项合并交易的可能性。"),
    
    # 29: 成交过程
    ("Bob took it from there, and on September 18, Al and I met in New  York. I had long been familiar with FlightSafety's business, and in  about 60 seconds I knew that Al was exactly our kind of manager. A month  later, we had a contract. Because Charlie and I wished to minimize the  issuance of Berkshire shares, the transaction we structured gave  FlightSafety shareholders a choice of cash or stock but carried terms  that encouraged those who were tax-indifferent to take cash. This nudge  led to about 51% of FlightSafety's shares being exchanged for cash, 41%  for Berkshire A and 8% for Berkshire B.",
     "Bob于是接手进行这个案子，在9月18日我和Al正式在纽约碰面，我对国际飞安这家公司的经营状况本来就相当熟悉，而在60秒内我马上就知道Al正是符合我们类型的经理人，一个月后，合约正式敲定，由于查理跟我希望能够尽量避免再发行伯克希尔的新股份，所以在这项交易中，虽然我们提供国际飞安原股东换取股票或现金两种选择，但是交易条件等于间接鼓励这些税负没有太大差异的股东选择领取现金，结果总计最后有51%股份领取现金，41%换得伯克希尔A级普通股，另外8%换得伯克希尔B级普通股。"),
    
    # 30: Al的故事
    ("Al has had a lifelong love affair with aviation and actually piloted  Charles Lindbergh. After a barnstorming career in the 1930s, he began  working for Juan Trippe, Pan Am's legendary chief. In 1951, while still  at Pan Am, Al founded FlightSafety, subsequently building it into a  simulator manufacturer and a worldwide trainer of pilots (single-engine,  helicopter, jet and marine). The company operates in 41 locations,  outfitted with 175 simulators of planes ranging from the very small, such  as Cessna 210s, to Boeing 747s. Simulators are not cheap - they can cost  as much as $19 million - so this business, unlike many of our  operations, is capital intensive. About half of the company's revenues  are derived from the training of corporate pilots, with most of the  balance coming from airlines and the military.",
     "Al一生热爱飞行，曾经驾驶过查理林登号，在经过1930年代轰轰烈烈的飞行事业之后，他开始担任泛美航空的机长，之后在1951年创立国际飞安公司，将这家公司塑造成飞行仿真器制造与飞行员训练的世界级领导公司(单引擎、直升机、客机与水上飞机)，营业据点遍布41个地方，拥有175座的飞行仿真器，大至波音747客机，小到Cessna 210型小飞机，大家要知道飞行仿真器的造价可不便宜，有的要价甚至高达1,900万美金，所以这一行不像我们原来拥有的其它事业，算是相当资本密集的，该公司大约有一半的营业收入来自于训练飞行员的收入，其余则来自于航空公司与军事单位。"),
    
    # 31: Al的年龄
    ("Al may be 79, but he looks and acts about 55. He will run  operations just as he has in the past: We never fool with success. I  have told him that though we don't believe in splitting Berkshire stock,  we will split his age 2-for-1 when he hits 100.",
     "Al今年虽然已经79岁，不过外表举止看起来像55岁，他将一如往常继续经营这家公司，我们从来不会把成功搞混，我甚至跟他开玩笑说，虽然我们从没想过将伯克希尔的股份予以分割，不过等他满100岁时，我们倒是可以考虑把他的年纪一分为二。"),
    
    # 32: 雇用政策
    ("An observer might conclude from our hiring practices that Charlie  and I were traumatized early in life by an EEOC bulletin on age  discrimination. The real explanation, however, is self-interest: It's  difficult to teach a new dog old tricks. The many Berkshire managers who  are past 70 hit home runs today at the same pace that long ago gave them  reputations as young slugging sensations. Therefore, to get a job with  us, just employ the tactic of the 76-year-old who persuaded a dazzling  beauty of 25 to marry him. \"How did you ever get her to accept?\" asked  his envious contemporaries. The comeback: \"I told her I was 86.\"",
     "有人可能会怀疑我们现在雇用人的政策，可能是缘于早期年龄歧视政策所受到的创伤，其实真正的原因乃是出于自私的观点，因为我们认为实在是很难教新狗老把戏！在伯克希尔，许多经理人虽然已经年过70，但是他们还是像年轻时一样活跃，频频击出全垒打，所以如果各位有意到本公司谋得一职，请记得运用一位高龄76岁老翁如何追到25岁年轻辣妹的技巧，当同年龄的同伴很钦羡地问他：你到底是如何说服对方同意的呢？他回答到：很简单，我告诉她我今年86岁！"),
    
    # 33: 分隔符
    ("\t* * * * * * * * * * * *",
     ""),
]

def fix_translations():
    """修复HTML中的翻译"""
    global html_content
    
    # 统计
    total_fixed = 0
    
    # 对每个双语块进行处理
    pattern = re.compile(
        r'(<div class="bilingual-block">\s*<div class="lang-block lang-en">.*?<span class="lang-label">English</span>\s*<blockquote>)(.*?)(</blockquote>\s*</div>\s*<div class="lang-block lang-cn">.*?<span class="lang-label">中文翻译</span>\s*<blockquote>)(.*?)(</blockquote>\s*</div>\s*</div>)',
        re.DOTALL
    )
    
    def replace_func(match):
        global total_fixed
        
        en_content = match.group(2)
        cn_content = match.group(4)
        
        # 检查是否需要修复（中文字符数少于英文字符数的50%）
        en_len = len(re.findall(r'[a-zA-Z]', en_content))
        cn_len = len(re.findall(r'[\u4e00-\u9fff]', cn_content))
        
        # 跳过空块、纯分隔符块、表格块
        en_stripped = re.sub(r'\s+', ' ', en_content).strip()
        if not en_stripped or en_stripped.replace('*', '').replace('-', '').replace('=', '').replace('.', '') == '':
            return match.group(0)
        
        # 如果英文是表格数据（包含数字和$符号），跳过
        if re.search(r'\$\d+.*\d{4}', en_stripped) or re.search(r'\d{4}.*\$', en_stripped):
            return match.group(0)
        
        # 如果比例低于50%且英文足够长，尝试使用参考翻译
        if en_len > 30 and cn_len < en_len * 0.5:
            # 在参考翻译中查找匹配
            for ref_en, ref_cn in REFERENCE_TRANSLATIONS:
                ref_en_clean = re.sub(r'\s+', ' ', ref_en).strip()
                en_clean = re.sub(r'\s+', ' ', en_stripped).strip()
                
                # 简单匹配：检查英文开头是否相同
                if en_clean[:50].lower() == ref_en_clean[:50].lower() and ref_cn:
                    total_fixed += 1
                    return match.group(1) + en_content + match.group(3) + ref_cn + match.group(5)
        
        return match.group(0)
    
    html_content = pattern.sub(replace_func, html_content)
    
    print(f"修复了 {total_fixed} 个双语块的翻译")
    return html_content

if __name__ == "__main__":
    print("开始修复1996年巴菲特致股东信的中文翻译...")
    fixed_content = fix_translations()
    
    # 保存修复后的文件
    output_path.write_text(fixed_content, encoding='utf-8')
    print(f"修复后的文件已保存到: {output_path}")
