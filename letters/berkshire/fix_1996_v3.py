#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复1996年巴菲特致股东信的中文翻译
直接翻译HTML中的英文原文
"""

import re
from pathlib import Path

# 使用相对路径
html_path = Path("1996.html")
content = html_path.read_text(encoding='utf-8')

def count_chinese_chars(text):
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    return len(chinese_pattern.findall(text))

def count_en_chars(text):
    en_pattern = re.compile(r'[a-zA-Z]')
    return len(en_pattern.findall(text))

# 直接从HTML提取并翻译的完整翻译库
TRANSLATIONS = {
    "To the Shareholders of Berkshire Hathaway Inc.": "致伯克希尔·哈撒韦公司的全体股东：",
    
    "Our gain in net worth during 1996 was $6.2 billion, or 36.1%. Per- share book value, however, grew by less, 31.8%, because the number of Berkshire shares increased: We issued stock in acquiring FlightSafety International and also sold new Class B shares.* Over the last 32 years (that is, since present management took over) per-share book value has grown from $19 to $19,011, or at a rate of 23.8% compounded annually.": 
        "1996年本公司的净值成长了36.1%，约62亿美元，不过每股净值仅成长了31.8%，原因在于去年我们以发行新股的方式并购了国际飞安公司，同时另外还追加发行了一些B级普通股，总计过去32年以来，也就是自从现有经营阶层接手之后，每股净值由当初的19元成长到现在的19,011美元，年复合成长率约为23.8%。",
    
    "Each Class B share has an economic interest equal to 1/30th of that possessed by a Class A share, which is the new designation for the only stock that Berkshire had outstanding before May 1996. Throughout this report, we state all per-share figures in terms of \"Class A equivalents,\" which are the sum of the Class A shares outstanding and 1/30th of the Class B shares outstanding.": 
        "B级普通股拥有A级普通股三十分之一的权利，这是从1996年五月开始伯克希尔新增的股份类型，在年报中所谓的每股数字系以A级普通股约当数为基础，亦即全部流通在外的A级普通股数加上流通在外的B级普通股数的三十分之一。",
    
    "* Each Class B share has an economic interest equal to 1/30th of that possessed by a Class A share, which is the new designation for the only stock that Berkshire had outstanding before May 1996. Throughout this report, we state all per-share figures in terms of \"Class A equivalents,\" which are the sum of the Class A shares outstanding and 1/30th of the Class B shares outstanding.": 
        "B级普通股拥有A级普通股三十分之一的权利，这是从1996年五月开始伯克希尔新增的股份类型，在年报中所谓的每股数字系以A级普通股约当数为基础，亦即全部流通在外的A级普通股数加上流通在外的B级普通股数的三十分之一。",
    
    "For technical reasons, we have restated our 1995 financial statements, a matter that requires me to present one of my less-than- thrilling explanations of accounting arcana. I'll make it brief.": 
        "基于技术性原因，我们必须将1995年的财务报表予以重编，这使我能够再度展现令人震惊的会计技巧，相信我，我会试着长话短说。",
    
    "The restatement was required because GEICO became a wholly-owned subsidiary of Berkshire on January 2, 1996, whereas it was previously classified as an investment. From an economic viewpoint - taking into account major tax efficiencies and other benefits we gained - the value of the 51% of GEICO we owned at year-end 1995 increased significantly when we acquired the remaining 49% of the company two days later. Accounting rules applicable to this type of \"step acquisition,\" however, required us to write down the value of our 51% at the time we moved to 100%. That writedown - which also, of course, reduced book value - amounted to $478.4 million. As a result, we now carry our original 51% of GEICO at a value that is both lower than its market value at the time we purchased the remaining 49% of the company and lower than the value at which we carry that 49% itself.": 
        "重编的原因是因为原先被列为被投资的盖可保险在1996年1月2日正式成为伯克希尔100%持有的子公司，从经济观点来看，考量可观的租税优惠与其它优点，我们原先在1995年底持有的51%的GEICO股权，其价值在二天后我们取得剩余49%股权之后大幅增加，然而对于这种渐进式购并，一般公认会计原则却要求我们必须在取得100%股权时，将原来账上51%的成本反向予以调减，使得账面价值减少为4.784亿美元，这结果使得原来51%股权的账面价值不但远低于后来49%股权的取得市价，也低于我们持有后来这49%股权的账面价值。",
    
    "There is an offset, however, to the reduction in book value I have just described: Twice during 1996 we issued Berkshire shares at a premium to book value, first in May when we sold the B shares for cash and again in December when we used both A and B shares as part-payment for FlightSafety. In total, the three non-operational items affecting book value contributed less than one percentage point to our 31.8% per- share gain last year.": 
        "不过除了刚刚提到净值的减少之外，我们在1996年两度溢价发行股份，第一次是在五月办理现金增资发行B级普通股，第二次是在十二月发行A级与B级普通股，以购并国际飞安公司，总的来说，以上三项非营业项目对于去年本公司31.8%的每股净值成长率的净影响还不到1%。",
    
    "I dwell on this rise in per-share book value because it roughly indicates our economic progress during the year. But, as Charlie Munger, Berkshire's Vice Chairman, and I have repeatedly told you, what counts at Berkshire is intrinsic value, not book value. The last time you got that message from us was in the Owner's Manual, sent to you in June after we issued the Class B shares. In that manual, we not only defined certain key terms - such as intrinsic value - but also set forth our economic principles.": 
        "今年我之所以一再强调每股净值，原因在于它大约就等于我们在去年的实质进展，不过就像是查理跟我一再提醒各位的，对伯克希尔来说，真正重要的不是账面价值，而是实质价值，最近一次跟各位提到是在今年六月本公司发行B级普通股时，在送给各位的股东手册当中，我们不但对于一些名词予以定义，诸如实质价值等，同时也揭露了我们的企业宗旨。",
    
    "For many years, we have listed these principles in the front of our annual report, but in this report, on pages 58 to 67, we reproduce the entire Owner's Manual. In this letter, we will occasionally refer to the manual so that we can avoid repeating certain definitions and explanations. For example, if you wish to brush up on \"intrinsic value,\" see pages 64 and 65.": 
        "多年来，我们在年报前头揭示这些宗旨，在这里我们偶尔也会提到股东手册，这样我们就可以不必再重复解释一些常用的名词，比如说如果你想要了解一下什么叫实质价值，建议大家可以再翻翻那本手册的第64、65页。",
    
    "Last year, for the first time, we supplied you with a table that Charlie and I believe will help anyone trying to estimate Berkshire's intrinsic value. In the updated version of that table, which follows, we trace two key indices of value. The first column lists our per-share ownership of investments (including cash and equivalents) and the second column shows our per-share earnings from Berkshire's operating businesses before taxes and purchase-accounting adjustments but after all interest and corporate overhead expenses. The operating-earnings column excludes all dividends, interest and capital gains that we realized from the investments presented in the first column. In effect, the two columns show what Berkshire would have reported had it been broken into two parts.": 
        "从去年开始我们首度提供给各位一张查理跟我本人认为可以帮助大家估计伯克希尔公司实质价值的表格，在下面这张经过更新资料的表上，我们可以发现到两项与价值相关的重要指针，第一栏是我们平均每股持有的投资金额(包含现金与约当现金)，第二栏则是每股在扣除利息与营业费用之后，来自本业的营业利益(但未扣除所得税与购买法会计调整数)，当然后者已经扣除了所有来自第一栏投资所贡献的股利收入、利息收入与资本利得，事实上，若是把伯克希尔拆成两部分的话，这两栏数字将分别代表这两个部门的损益绩效。",
    
    "As the table tells you, our investments per share increased in 1996 by 29.0% and our non-investment earnings grew by 63.2%. Our goal is to keep the numbers in both columns moving ahead at a reasonable (or, better yet, unreasonable) pace.": 
        "从这张表大家可以看出，我们1996年的每股投资金额增加了29%，而非投资的本业盈余则增加了63.2%，我们的目标是让这两栏的数字以合理的速度稳定地成长，当然若是偶尔能以不合理的速度暴增也不错。",
    
    "Our expectations, however, are tempered by two realities. First, our past rates of growth cannot be matched nor even approached: Berkshire's equity capital is now large - in fact, fewer than ten businesses in America have capital larger - and an abundance of funds tends to dampen returns. Second, whatever our rate of progress, it will not be smooth: Year-to-year moves in the first column of the table above will be influenced in a major way by fluctuations in securities markets; the figures in the second column will be affected by wide swings in the profitability of our catastrophe-reinsurance business.": 
        "不过这样的预期可能会受到两项现实的因素所干扰，首先，我们很难再达到或接近过去那样高的成长速度，原因在于伯克希尔现在的资本规模实在是太庞大了，事实上以我们现在的资本规模已经可以排在全美企业的前十名，过多的资金一定会影响到整体的报酬率，第二点，不管成长的速度如何，铁定很难以平稳的速度增加，第一栏的数字将很容易随着股市大环境上下波动，第二栏的数字则会跟着超级灾害再保业务获利的不稳定变动而变化。",
    
    "In the table, the donations made pursuant to our shareholder- designated contributions program are charged against the second column, though we view them as a shareholder benefit rather than as an expense. All other corporate expenses are also charged against the second column. These costs may be lower than those of any other large American corporation: Our after-tax headquarters expense amounts to less than two basis points (1/50th of 1%) measured against net worth. Even so, Charlie used to think this expense percentage outrageously high, blaming it on my use of Berkshire's corporate jet, The Indefensible. But Charlie has recently experienced a \"counter-revelation\": With our purchase of FlightSafety, whose major activity is the training of corporate pilots, he now rhapsodizes at the mere mention of jets.": 
        "在这张表中，股东指定捐赠的款项被列为第二栏的减项，虽然我们将之视为股东的福利而非支出，企业其它的支出同样也被放在第二栏当作减项，这些开支远低于其它美国大企业的平均水准，每年我们企业总部的费用占净值的比率大约不到万分之五，即便如此查理还是认为这样的比率高得离谱，我想主要要怪罪于我个人所使用的伯克希尔企业专机-无可辩解号，不过最近在我们买下国际飞安-这家专门负责训练飞行的公司之后，查理的态度有了180度的转变，现在只要一提到飞机他就狂乐不已。",
    
    "Seriously, costs matter. For example, equity mutual funds incur corporate expenses - largely payments to the funds' managers - that average about 100 basis points, a levy likely to cut the returns their investors earn by 10% or more over time. Charlie and I make no promises about Berkshire's results. We do promise you, however, that virtually all of the gains Berkshire makes will end up with shareholders. We are here to make money with you, not off you.": 
        "认真的说，控制成本开支绝对重要，举例来说很多共同基金每年的营业费用大多在2%上下，这等于间接剥削了投资人将近10%的投资报酬，虽然查理跟我不敢向各位保证我们的投资绩效，但我们却可以向各位打包票，伯克希尔所赚的每一分钱一定会分文不差地落入股东的口袋里，我们是来帮各位赚钱，而不是帮各位花钱的。",
    
    "The Relationship of Intrinsic Value to Market Price": "实质价值与股票市价的关系",
    
    "In last year's letter, with Berkshire shares selling at $36,000, I told you: (1) Berkshire's gain in market value in recent years had outstripped its gain in intrinsic value, even though the latter gain had been highly satisfactory; (2) that kind of overperformance could not continue indefinitely; (3) Charlie and I did not at that moment consider Berkshire to be undervalued.": 
        "去年当伯克希尔的股价约在36,000美元时，我曾向各位报告过(1)伯克希尔这几年的股价表现远超越实质价值，虽然后者的成长幅度也相当令人满意，(2)这样的情况不可能无限制地持续下去，(3)查理跟我不认为当时伯克希尔的价值有被低估的可能性。",
    
    "Since I set down those cautions, Berkshire's intrinsic value has increased very significantly - aided in a major way by a stunning performance at GEICO that I will tell you more about later - while the market price of our shares has changed little. This, of course, means that in 1996 Berkshire's stock underperformed the business. Consequently, today's price/value relationship is both much different from what it was a year ago and, as Charlie and I see it, more appropriate.": 
        "自从我下了这些批注之后，伯克希尔的实质价值又大幅地增加了，主要的原因在于盖可惊人的表现(关于这点在后面还会向大家详细报告)，而在此同时伯克希尔的股价却维持不动，这代表在1996年伯克希尔的实质价值表现优于股价，也就是说，在今日伯克希尔的价格/价值比比起一年以前而言，又有很大的不同，这同时也是查理跟我认为比较合理的情况。",
    
    "Over time, the aggregate gains made by Berkshire shareholders must of necessity match the business gains of the company. When the stock temporarily overperforms or underperforms the business, a limited number of shareholders - either sellers or buyers - receive outsized benefits at the expense of those they trade with. Generally, the sophisticated have an edge over the innocents in this game.": 
        "就长期而言，伯克希尔股东的整体利得一定会与企业经营的获利一致，当公司股价的表现暂时优于或劣于企业经营时，少部分的股东-不管是买进的人或是卖出的人，将会因为做出这样的举动而从交易的对方身上占到一些便宜，通常来说，都是老经验的一方在这场游戏中占上风。",
    
    "Though our primary goal is to maximize the amount that our shareholders, in total, reap from their ownership of Berkshire, we wish also to minimize the benefits going to some shareholders at the expense of others. These are goals we would have were we managing a family partnership, and we believe they make equal sense for the manager of a public company. In a partnership, fairness requires that partnership interests be valued equitably when partners enter or exit; in a public company, fairness prevails when market price and intrinsic value are in sync. Obviously, they won't always meet that ideal, but a manager - by his policies and communications - can do much to foster equity.": 
        "虽然我们主要的目标是希望让伯克希尔的股东经由持有公司所有权所获得的利益极大化，但在此同时我们也期望能让一些股东从其它股东身上所占到的便宜能够极小化，我想这是一般人在经营家族企业时相当重视的，不过我们相信这也适用在上市公司的经营之上，对合伙企业来说，合伙权益在合伙人加入或退出时必须能够以合理的方式评量，才能维持公平，同样地，对于上市公司来说，惟有让公司的股价与实质价值一致，公司股东的公平性才得以维持，当然很明显，这样理想的情况很难一直维持，不过身为公司经理人可以透过其政策与沟通的方式来大力维持这样的公平性。",
    
    "Of course, the longer a shareholder holds his shares, the more bearing Berkshire's business results will have on his financial experience - and the less it will matter what premium or discount to intrinsic value prevails when he buys and sells his stock. That's one reason we hope to attract owners with long-term horizons. Overall, I think we have succeeded in that pursuit. Berkshire probably ranks number one among large American corporations in the percentage of its shares held by owners with a long-term view.": 
        "当然股东持有股份的时间越长，那么伯克希尔本身的表现与他的投资经验就会越接近，而他买进或卖出股份时的价格相较于实质价值是折价或溢价的影响程度也就越小，这也是为什么我们希望能够吸引具有长期投资意愿的股东加入的原因之一，总的来说，我认为就这点而言，我们算是做的相当成功，伯克希尔大概是所有美国大企业中拥有最多具长期投资观点股东的公司。",
    
    "Acquisitions of 1996": "1996年的并购案",
    
    "We made two acquisitions in 1996, both possessing exactly the qualities we seek - excellent business economics and an outstanding manager.": 
        "我们在1996年进行了两件并购案，两者皆拥有我们想要的特质-那就是绝佳的竞争优势与优秀的经理人。",
    
    "The first acquisition was Kansas Bankers Surety (KBS), an insurance company whose name describes its specialty. The company, which does business in 22 states, has an extraordinary underwriting record, achieved through the efforts of Don Towle, an extraordinary manager. Don has developed first-hand relationships with hundreds of bankers and knows every detail of his operation. He thinks of himself as running a company that is \"his,\" an attitude we treasure at Berkshire. Because of its relatively small size, we placed KBS with Wesco, our 80%-owned subsidiary, which has wanted to expand its insurance operations.": 
        "第一桩购并案是堪萨斯银行家保险-从字面上可知，这是一家专门提供银行业者保险的保险公司，在全美22个州从事相关业务，拥有相当不错的承保记录，全仰赖Don Towle这位杰出的经理人的努力，Don与上百位银行家皆保持良好的关系，而且也了解他所从事业务的每一项细节，那种感觉就好象是在经营\"自己\"的事业一样，这种精神是伯克希尔最欣赏的，由于它的规模不太大，同时正好伯克希尔持有80%股权的Wesco有意拓展保险事业，所以我们决定把它摆在Wesco之下成为其子公司。",
    
    "You might be interested in the carefully-crafted and sophisticated acquisition strategy that allowed Berkshire to nab this deal. Early in 1996 I was invited to the 40th birthday party of my nephew's wife, Jane Rogers. My taste for social events being low, I immediately, and in my standard, gracious way, began to invent reasons for skipping the event. The party planners then countered brilliantly by offering me a seat next to a man I always enjoy, Jane's dad, Roy Dinsdale - so I went.": 
        "大家或许会对我们这次精心设计的购并计划感到兴趣，在1996年初我受邀参加侄媳妇Jane40岁的生日宴会，由于我个人对于社交活动通常不太感兴趣，所以很自然地我按照惯例想出许多理由以婉拒这项邀请，不过对方显然有备而来，特别将我安排在另外一位我极有兴趣打交道的对象-Roy Dinsdale（Jane的父亲）的旁边，此举使得我无法拒绝而欣然赴会。",
    
    "The party took place on January 26. Though the music was loud - Why must bands play as if they will be paid by the decibel? - I just managed to hear Roy say he'd come from a directors meeting at Kansas Bankers Surety, a company I'd always admired. I shouted back that he should let me know if it ever became available for purchase.": 
        "生日宴会在1月26日举行，虽然当时现场音乐震耳欲聋(我实在搞不懂为何乐队总是要弹得那么大声，难道他们的出场费是按照分贝数计算的吗?)，不过我还是听到Roy说他刚参加完堪萨斯银行家保险的董事会，这是我一直相当欣赏的一家公司，我大声地响应他说，如果这家公司有意出售的话，记得一定要通知我。",
    
    "On February 12, I got the following letter from Roy: \"Dear Warren: Enclosed is the annual financial information on Kansas Bankers Surety. This is the company that we talked about at Janie's party. If I can be of any further help, please let me know.\" On February 13, I told Roy we would pay $75 million for the company - and before long we had a deal. I'm now scheming to get invited to Jane's next party.": 
        "2月12日我收到一封Roy的来函，上面写到：亲爱的沃伦，随函附送一份堪萨斯银行家保险的年度财务报表，就是上次在Jane的生日宴会上提到的那一家公司，如果你有任何需要，请务必让我知道。2月13日，我告诉Roy愿意出7,500万美元买下这家公司，不久之后，整个交易就搞定，现在的我正盘算明年还要再参加Jane的生日宴会。",
    
    "Our other acquisition in 1996 - FlightSafety International, the world's leader in the training of pilots - was far larger, at about $1.5 billion, but had an equally serendipitous origin. The heroes of this story are first, Richard Sercer, a Tucson aviation consultant, and second, his wife, Alma Murphy, an ophthalmology graduate of Harvard Medical School, who in 1990 wore down her husband's reluctance and got him to buy Berkshire stock. Since then, the two have attended all our Annual Meetings, but I didn't get to know them personally.": 
        "1996年发生的另一件购并案，全世界最大的飞行员训练公司-国际飞安公司，其规模比起前一个案子要大得多了，总金额高达15亿美元，不过这个案子发生的过程一样充满戏剧性，本案的功臣首推Richard Sercer-他是塔克森市的飞行顾问，当然还要归功于他的妻子-Alma Murphy，哈佛医学院眼科学系毕业的她好不容易在1990年说服她的丈夫买进伯克希尔的股份，而且在那之后每年都到奥玛哈参加我们的股东会，只是我一直没有机会与他们认识。",
    
    "Fortunately, Richard had also been a long-time shareholder of FlightSafety, and it occurred to him last year that the two companies would make a good fit. He knew our acquisition criteria, and he thought that Al Ueltschi, FlightSafety's 79-year-old CEO, might want to make a deal that would both give him a home for his company and a security in payment that he would feel comfortable owning throughout his lifetime. So in July, Richard wrote Bob Denham, CEO of Salomon Inc, suggesting that he explore the possibility of a merger.": 
        "碰巧的是，Richard同时也是国际飞安公司长期投资的股东，刚好在去年他认为这两家公司应该有机会可以做一个结合，他相当了解伯克希尔购并公司的标准，同时也知道国际飞安79岁的总裁-Al Ueltschi想要为自己的公司找一个理想的归宿，好为自己的股权找到一层保障，所以就在七月份，Richard写信给所罗门公司的总裁-Bob Denham请他研究这项合并交易的可能性。",
    
    "Bob took it from there, and on September 18, Al and I met in New York. I had long been familiar with FlightSafety's business, and in about 60 seconds I knew that Al was exactly our kind of manager. A month later, we had a contract. Because Charlie and I wished to minimize the issuance of Berkshire shares, the transaction we structured gave FlightSafety shareholders a choice of cash or stock but carried terms that encouraged those who were tax-indifferent to take cash. This nudge led to about 51% of FlightSafety's shares being exchanged for cash, 41% for Berkshire A and 8% for Berkshire B.": 
        "Bob于是接手进行这个案子，在9月18日我和Al正式在纽约碰面，我对国际飞安这家公司的经营状况本来就相当熟悉，而在60秒内我马上就知道Al正是符合我们类型的经理人，一个月后，合约正式敲定，由于查理跟我希望能够尽量避免再发行伯克希尔的新股份，所以在这项交易中，虽然我们提供国际飞安原股东换取股票或现金两种选择，但是交易条件等于间接鼓励这些税负没有太大差异的股东选择领取现金，结果总计最后有51%股份领取现金，41%换得伯克希尔A级普通股，另外8%换得伯克希尔B级普通股。",
    
    "Al has had a lifelong love affair with aviation and actually piloted Charles Lindbergh. After a barnstorming career in the 1930s, he began working for Juan Trippe, Pan Am's legendary chief. In 1951, while still at Pan Am, Al founded FlightSafety, subsequently building it into a simulator manufacturer and a worldwide trainer of pilots (single-engine, helicopter, jet and marine). The company operates in 41 locations, outfitted with 175 simulators of planes ranging from the very small, such as Cessna 210s, to Boeing 747s. Simulators are not cheap - they can cost as much as $19 million - so this business, unlike many of our operations, is capital intensive. About half of the company's revenues are derived from the training of corporate pilots, with most of the balance coming from airlines and the military.": 
        "Al一生热爱飞行，曾经驾驶过查理林登号，在经过1930年代轰轰烈烈的飞行事业之后，他开始担任泛美航空的机长，之后在1951年创立国际飞安公司，将这家公司塑造成飞行仿真器制造与飞行员训练的世界级领导公司(单引擎、直升机、客机与水上飞机)，营业据点遍布41个地方，拥有175座的飞行仿真器，大至波音747客机，小到Cessna 210型小飞机，大家要知道飞行仿真器的造价可不便宜，有的要价甚至高达1,900万美金，所以这一行不像我们原来拥有的其它事业，算是相当资本密集的，该公司大约有一半的营业收入来自于训练飞行员的收入，其余则来自于航空公司与军事单位。",
    
    "Al may be 79, but he looks and acts about 55. He will run operations just as he has in the past: We never fool with success. I have told him that though we don't believe in splitting Berkshire stock, we will split his age 2-for-1 when he hits 100.": 
        "Al今年虽然已经79岁，不过外表举止看起来像55岁，他将一如往常继续经营这家公司，我们从来不会把成功搞混，我甚至跟他开玩笑说，虽然我们从没想过将伯克希尔的股份予以分割，不过等他满100岁时，我们倒是可以考虑把他的年纪一分为二。",
    
    "An observer might conclude from our hiring practices that Charlie and I were traumatized early in life by an EEOC bulletin on age discrimination. The real explanation, however, is self-interest: It's difficult to teach a new dog old tricks. The many Berkshire managers who are past 70 hit home runs today at the same pace that long ago gave them reputations as young slugging sensations. Therefore, to get a job with us, just employ the tactic of the 76-year-old who persuaded a dazzling beauty of 25 to marry him. \"How did you ever get her to accept?\" asked his envious contemporaries. The comeback: \"I told her I was 86.\"": 
        "有人可能会怀疑我们现在雇用人的政策，可能是缘于早期年龄歧视政策所受到的创伤，其实真正的原因乃是出于自私的观点，因为我们认为实在是很难教新狗老把戏！在伯克希尔，许多经理人虽然已经年过70，但是他们还是像年轻时一样活跃，频频击出全垒打，所以如果各位有意到本公司谋得一职，请记得运用一位高龄76岁老翁如何追到25岁年轻辣妹的技巧，当同年龄的同伴很钦羡地问他：你到底是如何说服对方同意的呢？他回答到：很简单，我告诉她我今年86岁！",
    
    "To begin with, float is money we hold but don't own. In an insurance operation, float arises because premiums are received before losses are paid.": 
        "首先，浮存金是一项我们持有但不属于我们的资金，在保险公司的营运中，浮存金的产生原因在于保险公司在真正支付损失理赔之前，一般会先向保户收取保费。",
    
    "Typically, the premiums that an insurer takes in do not cover the losses and expenses it eventually must pay. That leaves it running an \"underwriting loss,\" which is the cost of float. An insurance business has value if its cost of float over time is less than the cost the company would otherwise incur to obtain funds. But the business is an albatross if the cost of its float is higher than market rates for money.": 
        "而通常保险业者收取的保费不足以因应最后支付出去的相关损失与费用，于是保险公司便会发生承保损失，这就是浮存金的成本，而当浮存金成本长期而言低于从其它管道取得资金的成本时，保险公司就有存在的价值，不过保险事业取得浮存金的成本若远高于资金市场利率时，它就像是一只在陆地上笨重的信天翁。",
    
    "As the numbers in the following table show, Berkshire's insurance business has been a huge winner. For the table, we have calculated our float - which we generate in large amounts relative to our premium volume - by adding loss reserves, loss adjustment reserves, funds held under reinsurance assumed and unearned premium reserves, and then subtracting agents' balances, prepaid acquisition costs, prepaid taxes and deferred charges applicable to assumed reinsurance. Our cost of float is determined by our underwriting loss or profit. In those years when we have had an underwriting profit, such as the last four, our cost of float has been negative. In effect, we have been paid for holding money.": 
        "不过，如下表所示，伯克希尔的保险业务可谓大获全胜。相对于总保费收入，我们的浮存金规模相当可观，而浮存金的成本取决于实际的承保损失或收益。",
    
    "Since 1967, when we entered the insurance business, our float has grown at an annual compounded rate of 22.3%. In more years than not, our cost of funds has been less than nothing. This access to \"free\" money has boosted Berkshire's performance in a major way. Moreover, our acquisition of GEICO materially increases the probability that we can continue to obtain \"free\" funds in increasing amounts.": 
        "自从1967年我们进军保险业以来，我们的浮存金每年以22.3%复合率增加，大部分的年度，我们的资金成本都在零以下，受惠于这些免费的资金，伯克希尔的绩效大大的提升了。更甚者，在完成对GEICO的并购之后，我们取得免费资金的成长速度又加快了许多。",
    
    "Super-Cat Insurance": "霹雳猫保险业务",
    
    "As in the past three years, we once again stress that the good results we are reporting for Berkshire stem in part from our super-cat business having a lucky year. In this operation, we sell policies that insurance and reinsurance companies buy to protect themselves from the effects of mega-catastrophes. Since truly major catastrophes are rare occurrences, our super-cat business can be expected to show large profits in most years - and to record a huge loss occasionally. In other words, the attractiveness of our super-cat business will take a great many years to measure. What you must understand, however, is that a truly terrible year in the super-cat business is not a possibility - it's a certainty. The only question is when it will come.": 
        "与过去三年一样，我们再次强调今年伯克希尔保险事业之所以能够有这么好的成绩，部分的原因要归功于霹雳猫业务又渡过幸运的一年，从事这类业务，我们出售保单给保险公司与再保公司以分散其面临超大型意外灾害所可能承担的风险，由于真正重大的灾害并不常发生，所以我们的霹雳猫业务有可能在连续几年赚大钱后，才突然发生重大的损失，换句话说，我们这项霹雳猫业务到底有多吸引人可能要花上好几年才有办法看得清，不过大家必须明了，所谓的重大损失的年头不是可能会发生，而是肯定会发生，唯一的问题是它什么时候会降临。",
    
    "I emphasize this lugubrious point because I would not want you to panic and sell your Berkshire stock upon hearing that some large catastrophe had cost us a significant amount. If you would tend to react that way, you should not own Berkshire shares now, just as you should entirely avoid owning stocks if a crashing market would lead you to panic and sell. Selling fine businesses on \"scary\" news is usually a bad decision. (Robert Woodruff, the business genius who built Coca-Cola over many decades and who owned a huge position in the company, was once asked when it might be a good time to sell Coke stock. Woodruff had a simple answer: \"I don't know. I've never sold any.\")": 
        "我之所以会把丑话说在前头，是因为我不希望大家那天突然听到伯克希尔因为某某大型意外灾害须理赔一大笔钱时，恐慌地拋售手中的持股，而如果届时你真的会有这种反应，那么你根本就不应该拥有本公司的股份，就像是如果你是那种碰到股市崩盘，会恐慌性的拋售手中股票的人，我建议你最好不要投资股票，听到坏消息而把手中的好股票卖掉通常不会是一个明智的决定。（数十年前创办可口可乐的天才企业家Robert Woodruff曾经被问到，什么情况下是出售可口可乐股票的好时机，Woodruff简短的回答到，我不知道，我从来就没有卖过！）。",
    
    "In our super-cat operation, our customers are insurers that are exposed to major earnings volatility and that wish to reduce it. The product we sell - for what we hope is an appropriate price - is our willingness to shift that volatility to our own books. Gyrations in Berkshire's earnings don't bother us in the least: Charlie and I would much rather earn a lumpy 15% over time than a smooth 12%. (After all, our earnings swing wildly on a daily and weekly basis - why should we demand that smoothness accompany each orbit that the earth makes of the sun?) We are most comfortable with that thinking, however, when we have shareholder/partners who can also accept volatility, and that's why we regularly repeat our cautions.": 
        "谈到霹雳猫保险业务，我们的客户主要是一些想要降低本身必须承担盈余变动剧烈风险的保险公司，而我们贩卖的产品——当然一定要以合理的价格，将这些盈余变动的风险转移到本公司的账上，因为我们对于伯克希尔公司盈余剧烈的变动一点都不会介意，查理跟我宁可接受上下变动但平均可达15%的结果，也不要平稳的12%。（就像是我们知道公司的盈余每天、每周都会变动，那么我们又何必强求公司的盈余变化一定要跟地球环绕太阳轨道的时间一致呢？）我想如果伯克希尔的股东合伙人也能有这样的看法，那么我们执行业务时便能更得心应手，而这也是为什么我们要一再提出相同警告的原因。",
    
    "We took on some major super-cat exposures during 1996. At mid-year we wrote a contract with Allstate that covers Florida hurricanes, and though there are no definitive records that would allow us to prove this point, we believe that to have then been the largest single catastrophe risk ever assumed by one company for its own account. Later in the year, however, we wrote a policy for the California Earthquake Authority that goes into effect on April 1, 1997, and that exposes us to a loss more than twice that possible under the Florida contract. Again we retained all the risk for our own account. Large as these coverages are, Berkshire's after-tax \"worst-case\" loss from a true mega-catastrophe is probably no more than $600 million, which is less than 3% of our book value and 1.5% of our market value. To gain some perspective on this exposure, look at the table on page 2 and note the much greater volatility that security markets have delivered us.": 
        "我们在1996年陆续接了好几件大业务，在年中我们与全美保险签约承保佛罗里达飓风险，虽然没有确切的资料可供左证，但我们相信这应该是单一公司独力承受单一风险的最高记录，接着到年底，我们又与加州地震局签约承保比佛罗里达飓风高出一倍的理赔上限，保单预计从1997年4月1日开始生效，再一次我们独立承揽所有的风险，虽然承保的金额相当庞大，但是即使在最坏的状况下，任何一件大型灾害的税后损失也不会超过六亿美元，大约不到伯克希尔净值的3%或市值的1.5%，大家要了解这类风险的影响性，比起股票市场变动对我们的影响性来说，前者可谓是小巫见大巫。",
    
    "In the super-cat business, we have three major competitive advantages. First, the parties buying reinsurance from us know that we both can and will pay under the most adverse of circumstances. Were a truly cataclysmic disaster to occur, it is not impossible that a financial panic would quickly follow. If that happened, there could well be respected reinsurers that would have difficulty paying at just the moment that their clients faced extraordinary needs. Indeed, one reason we never \"lay off\" part of the risks we insure is that we have reservations about our ability to collect from others when disaster strikes. When it's Berkshire promising, insureds know with certainty that they can collect promptly.": 
        "在霹雳猫保险业务，我们主要有三项竞争优势，首先向我们投保再保险的客户都知道我们有能力，也会在最糟糕的情况下履约付款，因为万一真的发生什么大的灾难，很难保证金融恐慌就不会接踵而至，届时在其客户最需要援助时，可能连一些原本享有盛誉的再保公司都拿不出钱来，而事实上我们之所以从来不将风险再转嫁出去的一个原因也是因为我们对于灾难发生时，其它保险公司能否顺利支付赔款的能力有所保留，反之只要是伯克希尔做出的保证，所有的保户都可以百分之百确定一定可以立即得到理赔。",
    
    "Our second advantage - somewhat related - is subtle but important. After a mega-catastrophe, insurers might well find it difficult to obtain reinsurance even though their need for coverage would then be particularly great. At such a time, Berkshire would without question have very substantial capacity available - but it will naturally be our long-standing clients that have first call on it. That business reality has made major insurers and reinsurers throughout the world realize the desirability of doing business with us. Indeed, we are currently getting sizable \"stand- by\" fees from reinsurers that are simply nailing down their ability to get coverage from us should the market tighten.": 
        "我们的第二项优势与上一条有些关联，虽然微妙却很重要。在遭遇一场超级大灾难之后，保险公司可能会发现，尽管他们此时对保险的需求特别大，但也很难获得再保险。这种情况下，伯克希尔公司毫无疑问会有非常大的承保能力——但自然会优先受理原来与我们有长期往来的客户。这个业务现实已使全世界的保险公司与再保公司了解到与我们维持往来的必要性，事实上，我们现在正从许多再保公司那里收取预备费，以防万一市场情况紧绷时，他们可以确保取得再保的优先机会。",
    
    "Our final competitive advantage is that we can provide dollar coverages of a size neither matched nor approached elsewhere in the industry. Insurers looking for huge covers know that a single call to Berkshire will produce a firm and immediate offering.": 
        "我们拥有的最后一项优势是我们能够提供别处得不到单一最高的投保上限，保险业者都知道只要打一通电话到伯克希尔，就可以立即得到确定满意的答复。",
    
    "A few facts about our exposure to California earthquakes - our largest risk - seem in order. The Northridge quake of 1994 laid homeowners' losses on insurers that greatly exceeded what computer models had told them to expect. Yet the intensity of that quake was mild compared to the \"worst-case\" possibility for California. Understandably, insurers became - ahem - shaken and started contemplating a retreat from writing earthquake coverage into their homeowners' policies.": 
        "关于我们最大的风险敞口——加州地震，似乎有必要介绍一些情况。1994年的北岭地震给保险公司造成的房屋业主损失大大超出了计算机模型的预期。然而这次地震的震级比起预估可能的最坏情况，还算是相对轻微的，所以可想而知某些保险业者肯定都吓坏了，因此开始考虑将地震险从他们的住宅险保单条款中撤掉。",
    
    "In a thoughtful response, Chuck Quackenbush, California's insurance commissioner, designed a new residential earthquake policy to be written by a state-sponsored insurer, The California Earthquake Authority. This entity, which went into operation on December 1, 1996, needed large layers of reinsurance - and that's where we came in. Berkshire's layer of approximately $1 billion will be called upon if the Authority's aggregate losses in the period ending March 31, 2001 exceed about $5 billion. (The press originally reported larger figures, but these would have applied only if all California insurers had entered into the arrangement; instead only 72% signed up.)": 
        "深富远见的加州保险专员Chuck Quackenbush立即规划出一张由加州地震局背后支持新的住宅地震保单，然而这项预计从1996年12月1日开始正式生效的措施极需要再保险的庇护，这时候就轮到我们上场了，伯克希尔总共提供10亿美元的再保险防护，当地震局在2001年3月31日之前因地震发生的损失超过50亿美元时（媒体原先报导的数字比这更高，不过那是在所有保险业者都一同加入时的情况，总计最后只有72%的业者参与签约）。",
    
    "So what are the true odds of our having to make a payout during the policy's term? We don't know - nor do we think computer models will help us, since we believe the precision they project is a chimera. In fact, such models can lull decision-makers into a false sense of security and thereby increase their chances of making a really huge mistake. We've already seen such debacles in both insurance and investments. Witness \"portfolio insurance,\" whose destructive effects in the 1987 market crash led one wag to observe that it was the computers that should have been jumping out of windows.": 
        "那么，在保单的有效期内，我们需要支付赔款的真实概率是多少呢？我们不知道——我们也不认为计算机模型会帮我们什么忙，因为我们相信计算机运算出来的预测根本就是垃圾，它们反而会让做决策的人误以为得到某种确定的假象，从而使得他们犯下大错的机会大增，过去不管是在保险或投资业者，这种离谱的情况屡见不鲜，看看投资组合保险在1987年股市大崩盘时所造成的惨况，有人开玩笑说，当时应该要跳楼的是计算机而不是那些被它所愚弄的人。",
    
    "Even if perfection in assessing risks is unattainable, insurers can underwrite sensibly. After all, you need not know a man's precise age to know that he is old enough to vote nor know his exact weight to recognize his need to diet. In insurance, it is essential to remember that virtually all surprises are unpleasant, and with that in mind we try to price our super-cat exposures so that about 90% of total premiums end up being eventually paid out in losses and expenses. Over time, we will find out how smart our pricing has been, but that will not be quickly. The super-cat business is just like the investment business in that it often takes a long time to find out whether you knew what you were doing.": 
        "虽然保险业者无法准确地评估风险到底有多大，不过我们却还是可以合理的接下保单，就像是你并不一定要真的知道一个人的实际年龄，才能判断他是否可以去投票或是一定要知道一个人几公斤重才认为他该不该减肥。同样的，从事保险这一行，大家必须谨记的是，基本上所有的意外都不会让人感到愉快，所以在接下保单时，我们心里早有预备，准备把90%的保费收入花在损失理赔与相关费用之上，慢慢的一段时间下来，我们就会发现，这样的订价是否合理，这绝对需要时间来证明，霹雳猫保险这一行就像是投资事业一样，绝对需要一段很长的时间，你才能确切的知道自己到底在干什么。",
    
    "What I can state with certainty, however, is that we have the best person in the world to run our super-cat business: Ajit Jain, whose value to Berkshire is simply enormous. In the reinsurance field, disastrous propositions abound. I know that because I personally embraced all too many of these in the 1970s and also because GEICO has a large runoff portfolio made up of foolish contracts written in the early-1980s, able though its then-management was. Ajit, I can assure you, won't make mistakes of this type.": 
        "不过有一点我绝对可以向各位保证，我们拥有全世界最优秀的霹雳猫保险专家，那就是Ajit Jain，他在伯克希尔的价值大到难以想象，在再保险这一行，恐怖的灾难时常发生，我很清楚的原因是我个人在1970年代就抱了不少个地雷，而盖可在1980年代初期，即使当时拥有最能干的经理人，也同样签了一堆愚蠢的保险合约，不过提到Ajit，我可以向各位保证，绝对不会再犯同样的错误。",
    
    "I have mentioned that a mega-catastrophe might cause a catastrophe in the financial markets, a possibility that is unlikely but not far-fetched. Were the catastrophe a quake in California of sufficient magnitude to tap our coverage, we would almost certainly be damaged in other ways as well. For example, See's, Wells Fargo and Freddie Mac could be hit hard. All in all, though, we can handle this aggregation of exposures.": 
        "不过另一方面我也说过，自然灾害的发生同样也会间接导致金融风暴的发生，这样的可能性不大，但也不是不可能，要是加州真的发生规模大到我们理赔上限的大地震，我们旗下其它事业也可能会受到严重的打击，比如说喜诗糖果、富国银行或房利美等，不过总的来说，我们应该可以妥善处理发生的状况。",
    
    "In this respect, as in others, we try to \"reverse engineer\" our future at Berkshire, bearing in mind Charlie's dictum: \"All I want to know is where I'm going to die so I'll never go there.\" (Inverting really works: Try singing country western songs backwards and you will quickly regain your house, your car and your wife.) If we can't tolerate a possible consequence, remote though it may be, we steer clear of planting its seeds. That is why we don't borrow big amounts and why we make sure that our super-cat business losses, large though the maximums may sound, will not put a major dent in Berkshire's intrinsic value.": 
        "就这方面而言，我们试着事先规划伯克希尔的未来，时时谨记查理常说的一句格言：\"希望能够知道自己最后会死在哪里，然后打死都不去那里！\"（事先回想真的有效，大家可以试着多唱唱以前流行的乡村歌曲，很快的你就会发现重新找回了你的房子、你的车子跟老婆），如果我们没办法承担可能的后果，不管其可能性有多小，那么我们就必须避免播下罪恶的种子。",
    
    "Insurance - GEICO and Other Primary Operations": "保险 —— GEICO及其他原保险业务",
    
    "When we moved to total ownership of GEICO early last year, our expectations were high - and they are all being exceeded. That is true from both a business and personal perspective: GEICO's operating chief, Tony Nicely, is a superb business manager and a delight to work with. Under almost any conditions, GEICO would be an exceptionally valuable asset. With Tony at the helm, it is reaching levels of performance that the organization would only a few years ago have thought impossible.": 
        "去年年初，当我们全资收购GEICO时，我们的期望很高——而现在，我们的期望被全面超越了。无论是从商业的角度，还是从个人的角度来看都是如此：GEICO的运营总监Tony Nicely，是一位非常出色的商业管理者，值得与之共事。在几乎任何条件下，GEICO都将是一项非常有价值的资产。在Tony的领导下，它正在达到几年前该组织认为不可能达到的绩效水平。",
    
    "There's nothing esoteric about GEICO's success: The company's competitive strength flows directly from its position as a low-cost operator. Low costs permit low prices, and low prices attract and retain good policyholders. The final segment of a virtuous circle is drawn when policyholders recommend us to their friends. GEICO gets more than one million referrals annually and these produce more than half of our new business, an advantage that gives us enormous savings in acquisition expenses - and that makes our costs still lower.": 
        "GEICO的成功并不神秘：该公司的竞争力直接源于其作为低成本经营者的地位。低成本带来低价格，低价格吸引并留住优秀的投保人。一旦这种良性循环运转起来，政策持有人就会向朋友推荐我们。GEICO每年获得超过一百万次的转介绍客户，而这些转介绍客户贡献了超过一半的新业务，这种优势为我们节省了大量的获客成本——而这也使得我们的成本进一步降低。",
    
    "This formula worked in spades for GEICO in 1996: Its voluntary auto policy count grew 10%. During the previous 20 years, the company's best-ever growth for a year had been 8%, a rate achieved only once. Better yet, the growth in voluntary policies accelerated during the year, led by major gains in the nonstandard market, which has been an underdeveloped area at GEICO. I focus here on voluntary policies because the involuntary business we get from assigned risk pools and the like is unprofitable. Growth in that sector is most unwelcome.": 
        "这个公式在1996年对GEICO产生了极佳的效果：其自愿汽车保单数量增长了10%。在此之前的20年里，该公司最好的年度增长率仅为8%，而且只达到过一次。更重要的是，增长率在全年都在加速，其中在非标准市场领域取得了重大进展，而这正是GEICO过去开发不足的领域。我在这里关注自愿保单的原因在于，我们从分配风险池等渠道获得的非自愿业务是亏损的，因此这类业务的增长是最不受欢迎的。",
    
    "GEICO's growth would mean nothing if it did not produce reasonable underwriting profits. Here, too, the news is good: Last year we hit our underwriting targets and then some. Our goal, however, is not to widen our profit margin but rather to enlarge the price advantage we offer customers. Given that strategy, we believe that 1997's growth will easily top that of last year.": 
        "如果不能产生合理的承保利润，GEICO的增长就毫无意义。这里也有好消息：去年，我们不仅实现了承保目标，还超出了一些。不过，我们的目标不是扩大利润率，而是扩大我们为客户提供的价格优势。鉴于这一策略，我们相信1997年的增长将轻松超过去年。",
    
    "We expect new competitors to enter the direct-response market, and some of our existing competitors are likely to expand geographically. Nonetheless, the economies of scale we enjoy should allow us to maintain or even widen the protective moat surrounding our economic castle. We do best on costs in geographical areas in which we enjoy high market penetration. As our policy count grows, concurrently delivering gains in penetration, we expect to drive costs materially lower. GEICO's sustainable cost advantage is what attracted me to the company way back in 1951, when the entire business was valued at $7 million. It is also why I felt Berkshire should pay $2.3 billion last year for the 49% of the company that we didn't then own.": 
        "我们预计会有新的竞争对手进入直复营销市场，我们现有的一些竞争对手也可能进行地域扩张。尽管如此，我们所享有的规模经济应该能够让我们保持甚至扩大围绕经济城堡的护城河。在我们拥有较高市场渗透率的地区，我们在成本方面做得最好。随着我们的保单数量增长，同时渗透率也随之提高，我们预计成本将大幅降低。GEICO可持续的成本优势，正是1951年吸引我投资这家公司的原因，当时整个公司的估值仅为700万美元。这也是为什么我觉得伯克希尔应该在去年为剩余49%的股权支付23亿美元的原因。",
    
    "Maximizing the results of a wonderful business requires management and focus. Lucky for us, we have in Tony a superb manager whose business focus never wavers. Wanting also to get the entire GEICO organization concentrating as he does, we needed a compensation plan that was itself sharply focused - and immediately after our purchase, we put one in.": 
        "想要让一家好公司的表现发挥到极致，必须依赖优秀的管理人员与明确的目标方向。很幸运的是，我们有Tony这样一位杰出的管理者，他对企业专注从未动摇。为了让整个GEICO组织像他一样专注，我们需要一个本身高度聚焦的薪酬计划——在我们的收购完成后，我们立即推出了这样一个计划。",
    
    "Today, the bonuses received by dozens of top executives, starting with Tony, are based upon only two key variables: (1) growth in voluntary auto policies and (2) underwriting profitability on \"seasoned\" auto business (meaning policies that have been on the books for more than one year). In addition, we use the same yardsticks to calculate the annual contribution to the company's profit-sharing plan. Everyone at GEICO knows what counts.": 
        "如今，Tony以及数十位高管能获得的奖金只基于两个关键变量：（1）自愿车险保单的增长；（2）成熟车险业务的承保盈利能力。此外，我们还使用相同的标准来计算公司利润分享计划的年度贡献。GEICO的每个人都知道什么才是真正重要的。",
    
    "The GEICO plan exemplifies Berkshire's incentive compensation principles: Goals should be (1) tailored to the economics of the specific operating business; (2) simple in character so that the degree to which they are being realized can be easily measured; and (3) directly related to the daily activities of plan participants.": 
        "GEICO这项计划充分说明了伯克希尔薪资奖励的原则，那就是必须要能够达到以下目标：（1）根据具体运营业务的经济特性量身定制；（2）简单明了，便于衡量目标的实现程度；以及（3）与计划参与者的日常活动直接相关。",
    
    "As a corollary, we shun \"lottery ticket\" arrangements, such as options on Berkshire shares, whose ultimate value - which could range from zero to huge - is totally out of the control of the person whose behavior we would like to affect. In our view, a system that produces quixotic payoffs will not only be wasteful for owners but may actually discourage the focused behavior we value in managers.": 
        "作为推论，我们回避类似彩票的安排，比如伯克希尔股票的期权，其最终价值——可能从零到巨额不等——完全不在我们希望影响其行为的人的控制之下。在我们看来，一种产生不稳定回报的制度不仅对所有者是浪费的，而且可能实际上会抑制我们在管理者身上所珍视的专注行为。",
    
    "Every quarter, all 9,000 GEICO associates can see the results that determine our profit-sharing plan contribution. In 1996, they enjoyed the experience because the plan literally went off the chart that had been constructed at the start of the year. Even I knew the answer to that problem: Enlarge the chart. Ultimately, the results called for a record contribution of 16.9% ($40 million), compared to a five-year average of less than 10% for the comparable plans previously in effect. Furthermore, at Berkshire, we never greet good work by raising the bar. If GEICO's performance continues to improve, we will happily keep on making larger charts.": 
        "每一季，GEICO公司总共9,000名的员工都可以看到根据盈余分配计划所计算出来的结果，1996年他们确实享受到这项成果，因为根据这项计划所计算出来的数字早已打破当初规划时的最高上限，连我也知道要如何解决这个问题，那就是把上限再扩大，到最后，员工总共分配到年度获利的16.9%，金额将近有4,000万美元，远高于过去五年平均不到10%的比率，同时在Berkshire对于员工辛勤工作的表现，我们绝对不会回以更高的门坎，如果GEICO的员工继续保持如此优异的表现，我们还会继续提高奖励的上限。",
    
    "Lou Simpson continues to manage GEICO's money in an outstanding manner: Last year, the equities in his portfolio outdid the S&P 500 by 6.2 percentage points. In Lou's part of GEICO's operation, we again tie compensation to performance - but to investment performance over a four-year period, not to underwriting results nor to the performance of GEICO as a whole. We think it foolish for an insurance company to pay bonuses that are tied to overall corporate results when great work on one side of the business - underwriting or investment - could conceivably be completely neutralized by bad work on the other. If you bat .350 at Berkshire, you can be sure you will get paid commensurately even if the rest of the team bats .200. In Lou and Tony, however, we are lucky to have Hall-of-Famers in both key positions.": 
        "Lou Simpson继续出色地管理着GEICO的资金：去年，他管理的股票投资组合比标准普尔500指数高出了6.2个百分点。在Lou负责的GEICO业务领域，我们仍然将薪酬与业绩挂钩——但是与四年期内的投资业绩挂钩，而非与承保业绩或GEICO整体业绩挂钩。我们认为，让保险公司支付与整体公司业绩挂钩的奖金是愚蠢的，因为在一个业务领域的出色工作可能会被另一个领域的糟糕表现完全抵消。如果你在伯克希尔的击球率达到.350，你可以确信你会得到与之相称的报酬，即使团队其他人的击球率仅为.200。然而，幸运的是，在Lou和Tony这两位关键职位上，我们都拥有名人堂级别的选手。",
    
    "Though they are, of course, smaller than GEICO, our other primary insurance operations turned in equally stunning results last year. National Indemnity's traditional business had a combined ratio of 74.2 and, as usual, developed a large amount of float compared to premium volume. Over the last three years, this segment of our business, run by Don Wurster, has had an average combined ratio of 83.0. Our homestate operation, managed by Rod Eldred, recorded a combined ratio of 87.1 even though it absorbed the expenses of expanding to new states. Rod's three-year combined ratio is an amazing 83.2. Berkshire's workers' compensation business, run out of California by Brad Kinstler, has now moved into six other states and, despite the costs of that expansion, again achieved an excellent underwriting profit. Finally, John Kizer, at Central States Indemnity, set new records for premium volume while generating good earnings from underwriting. In aggregate, our smaller insurance operations (now including Kansas Bankers Surety) have an underwriting record virtually unmatched in the industry. Don, Rod, Brad and John have all created significant value for Berkshire, and we believe there is more to come.": 
        "虽然比起GEICO，我们其它主要保险事业规模要小得多，但他们在去年同样缴出惊人的成绩单。国家险的传统业务综合成本率为74.2，与往常一样，与保费规模相比，产生了大量的浮存金。在过去三年中，由Don Wurster运营的这一业务板块，平均综合成本率为83.0。我们的homestate业务，由Rod Eldred管理，即使吸收了新州扩张的费用，仍录得87.1的综合成本率。Rod的三年综合成本率为惊人的83.2。伯克希尔的工伤险业务，由加州的Brad Kinstler负责，现已扩展到其他六个州，尽管扩张成本不菲，但再次取得了优异的承保利润。最后，Central States Indemnity的John Kizer，在保费规模创历史新高的同时，也取得了良好的承保收益。总体而言，我们较小的保险业务的承保记录几乎在行业中无与伦比。Don、Rod、Brad和John都为伯克希尔创造了重大价值，我们相信未来还会有更多贡献。",
    
    "Taxes": "税务问题",
    
    "In 1961, President Kennedy said that we should ask not what our country can do for us, but rather ask what we can do for our country. Last year we decided to give his suggestion a try - and who says it never hurts to ask? We were told to mail $860 million in income taxes to the U.S. Treasury.": 
        "1961年，肯尼迪总统曾说过一句名言。去年，我们决定践行这一理念。最终，我们向美国国库缴纳了8.6亿美元的所得税。",
    
    "Here's a little perspective on that figure: If an equal amount had been paid by only 2,000 other taxpayers, the government would have had a balanced budget in 1996 without needing a dime of taxes - income or Social Security or what have you - from any other American. Berkshire shareholders can truly say, \"I gave at the office.\"": 
        "这个数字究竟有多大？如果全美国能有2,000家像伯克希尔这样的纳税人，那么美国国库无需再征收其他任何所得税，1996年的预算就能实现收支平衡。",
    
    "Charlie and I believe that large tax payments by Berkshire are entirely fitting. The contribution we thus make to society's well-being is at most only proportional to its contribution to ours. Berkshire prospers in America as it would nowhere else.": 
        "查理和我完全接受伯克希尔需支付如此高额的税负。我们深知，自己对社会的贡献远不及社会给予我们的馈赠。",
    
    "Sources of Reported Earnings": "报告收益的来源",
    
    "The table that follows shows the main sources of Berkshire's reported earnings. In this presentation, purchase-accounting adjustments are not assigned to the specific businesses to which they apply, but are instead aggregated and shown separately. This procedure lets you view the earnings of our businesses as they would have been reported had we not purchased them. For the reasons discussed on pages 65 and 66, this form of presentation seems to us to be more useful to investors and managers than one utilizing generally-accepted accounting principles (GAAP), which require purchase-premiums to be charged off business-by-business. The total earnings we show in the table are, of course, identical to the GAAP total in our audited financial statements.": 
        "下表显示了伯克希尔报告收益的主要来源。在这个表述中，购买法会计调整不分配给所适用的特定业务，而是汇总单独列示。这种程序让你能够以如果我们没有收购这些企业，它们本来会被报告的方式来查看我们企业的收益。由于第65和66页讨论的原因，这种形式的表述在我们看来对投资者和管理者都更有用，而不是使用一般公认会计原则（GAAP），后者要求将收购溢价逐个业务冲销。当然，我们在表格中显示的总收益与审计财务报表中的GAAP总额相同。",
    
    "Though infrequently Berkshire reports earnings calculated by strict GAAP convention, Charlie and I believe that certain non-GAAP measurements are critically important to evaluating Berkshire's economic performance. We call these \"look-through\" earnings. To calculate them, you (1) begin with reported operating earnings; (2) add your share of the retained operating earnings of major investees that, under GAAP accounting, are not reflected in our profits, less; (3) an allowance for the tax that would be paid by Berkshire if these retained earnings of investees had instead been distributed to us. When tabulating \"operating earnings\" here, we exclude purchase-accounting adjustments as well as capital gains and other major non-recurring items.": 
        "虽然伯克希尔很少按公认会计准则（GAAP）来严格计算报告盈余，但查理和我相信，有一些数字虽然不属于GAAP的范畴，却对评估伯克希尔的经营成果至关重要。我们将它们称为\"透视\"盈余。计算方法如下：（1）从报告的营业利润开始；（2）加上我们按比例分享的主要被投资公司保留的营业利润，这些利润在GAAP会计制度下不会反映在我们的利润中，减去；（3）如果这些被投资公司的留存收益被分配给我们，伯克希尔需要支付的税款（按14%的税率计算）。",
    
    "The following table sets forth our 1996 look-through earnings, though I warn you that the figures can be no more than approximate, since they are based on a number of judgment calls. (The dividends paid to us by these investees have been included in the operating earnings itemized on page 12, mostly under \"Insurance Group: Net Investment Income.\")": 
        "下表列出了1996年的透视收益，不过我需要提醒大家，这些数字只是近似值，因为它们基于多项主观判断。（被投资公司支付给我们的股息已包含在第12页所列的经营收益项目中，大部分在\"保险集团：净投资收益\"项下。）",
    
    "Common Stock Investments": "股票投资",
    
    "Below we present our common stock investments. Those with a market value of more than $500 million are itemized.": 
        "下表是我们市价超过五亿美元以上的普通股投资。",
    
    "* Represents tax-basis cost which, in aggregate, is $1.2 billion less than GAAP cost.": 
        "* 代表税基成本，合计比GAAP成本低12亿美元。",
    
    "Our portfolio shows little change: We continue to make more money when snoring than when active.": 
        "1996年，我们的投资组合变化不大。我们呆坐不动赚的钱，比我们忙忙碌碌赚来的更多。",
    
    "Inactivity strikes us as intelligent behavior. Neither we nor most business managers would dream of feverishly trading highly-profitable subsidiaries because a small move in the Federal Reserve's discount rate was predicted or because some Wall Street pundit had reversed his views on the market. Why, then, should we behave differently with our minority positions in wonderful businesses? The art of investing in public companies successfully is little different from the art of successfully acquiring subsidiaries. In each case you simply want to acquire, at a sensible price, a business with excellent economics and able, honest management. Thereafter, you need only monitor whether these qualities are being preserved.": 
        "我们觉得持仓不动是明智的行为。我们和大多数企业经理一样，不会因为市场预测美联储可能加息或降息，或是因为某些华尔街权威人士改变了对市场的看法，就狂热地买卖利润丰厚的下属子公司股权。那么，我们为什么要以不同的方式对待自己持有的优秀公司少数股权呢？上市公司投资的成功之道与并购子公司的成功之道并没有什么不同。在两种情况下，你都需要只是以合理的价格买进一家拥有优秀经济特性和诚实能干的管理层的企业。此后，你只需留意这些特质是否仍然存在。",
    
    "When carried out capably, an investment strategy of that type will often result in its practitioner owning a few securities that will come to represent a very large portion of his portfolio. This investor would get a similar result if he followed a policy of purchasing an interest in, say, 20% of the future earnings of a number of outstanding college basketball stars. A handful of these would go on to achieve NBA stardom, and the investor's take from them would soon dominate his royalty stream. To suggest that this investor should sell off portions of his most successful investments simply because they have come to dominate his portfolio is akin to suggesting that the Bulls trade Michael Jordan because he has become so important to the team.": 
        "如果执行得当，这种投资策略通常会导致投资者持有少数几种证券，而这些证券将占据其投资组合的很大一部分。这位投资者如果采取购买一批杰出大学篮球明星未来收入20%权益的策略，也会得到类似的结果。其中少数人后来成为了NBA的明星，投资者从他们身上获得的收益很快就成为他投资王国的主要\"税收\"收入。建议这位投资者仅仅因为最成功的投资已经占据投资组合的主导地位就卖出部分持仓，这种建议就好比建议公牛队交易迈克尔·乔丹，因为他对球队已经变得太过重要。",
    
    "In studying the investments we have made in both subsidiary companies and common stocks, you will see that we favor businesses and industries unlikely to experience major change. The reason for that is simple: Making either type of purchase, we are searching for operations that we believe are virtually certain to possess enormous competitive strength ten or twenty years from now. A fast-changing industry environment may offer the chance for huge wins, but it precludes the certainty we seek.": 
        "在研究我们无论是收购子公司还是对上市公司股票的投资，你都会发现我们偏爱那些不太可能经历重大变化的企业和行业。原因很简单：我们寻找的是我们相信在10年或20年后几乎肯定会拥有巨大竞争优势的企业。一个快速变化的行业环境可能会提供获得巨额回报的机会，但它排除了我们所需要的确定性。",
    
    "I should emphasize that, as citizens, Charlie and I welcome change: Fresh ideas, new products, innovative processes and the like cause our country's standard of living to rise, and that's clearly good. As investors, however, our reaction to a fermenting industry is much like our attitude toward space exploration: We applaud the endeavor but prefer to skip the ride.": 
        "我应该强调一点：作为普通公民，查理和我欢迎创新和改变。新想法、新产品和创新等提高了我们国家的生活水平，这显然是好事。然而，作为投资者，我们对正在发生巨变的行业做出的反应，类似我们对太空旅行的态度：我们赞赏这种努力，但更愿意跳过这段旅程。",
    
    "Obviously all businesses change to some extent. Today, See's is different in many ways from what it was in 1972 when we bought it: It offers a different assortment of candy, employs different machinery and sells through different distribution channels. But the reasons why people today buy boxed chocolates, and why they buy them from us rather than from someone else, are virtually unchanged from what they were in the 1920s when the See family was building the business. Moreover, these motivations are not likely to change over the next 20 years, or even 50.": 
        "当然，任何企业或多或少都会发生改变。今天，喜诗糖果在许多方面都与1972年我们收购它时不同：如今它生产不同种类的糖果，使用不同的机器，并通过不同的分销渠道销售。但今天人们购买盒装巧克力的原因，以及他们从我们这里而不是从别人那里购买的原因，与上世纪20年代喜诗家族创办企业时几乎没有改变。此外，这些购买动机在未来20年甚至50年内也不太可能改变。",
    
    "We look for similar predictability in marketable securities. Take Coca-Cola: The zeal and imagination with which Coke products are sold has surged under Roberto Goizueta, who has done an absolutely incredible job in creating value for his shareholders. Aided by Don Keough and Doug Ivester, Roberto has rethought and improved every aspect of the company. But the fundamentals of the business - the qualities that underlie Coke's competitive dominance and stunning economics - have remained constant through the years.": 
        "我们在有价证券投资中寻找类似的可预测性。以可口可乐为例：在罗伯托·古崔塔的领导下，可口可乐产品的销售热情和想象力都大大增强，他在为股东创造价值方面做得非常出色。在Don Keough与Doug Ivester的协助之下，古崔塔从头到尾重新塑造了公司的每一个方面。但是，这项业务的基础——支撑可口可乐竞争主导地位和经济优势的品质——这些年来一直保持不变。",
    
    "I was recently studying the 1896 report of Coke (and you think that you are behind in your reading!). At that time Coke, though it was already the leading soft drink, had been around for only a decade. But its blueprint for the next 100 years was already drawn. Reporting sales of $148,000 that year, Asa Candler, the company's president, said: \"We have not lagged in our efforts to go into all the world teaching that Coca-Cola is the article, par excellence, for the health and good feeling of all people.\" Though \"health\" may have been a reach, I love the fact that Coke still relies on Candler's basic theme today - a century later. Candler went on to say, just as Roberto could now, \"No article of like character has ever so firmly entrenched itself in public favor.\" Sales of syrup that year, incidentally, were 116,492 gallons versus about 3.2 billion in 1996.": 
        "最近我正在研读可口可乐1896年的年报（所以大家现在看我们的年报应该还不嫌太晚）。虽然当时可口可乐已经成为冷饮市场的领导者，但那也不过只有十年的光景。然而在当时，该公司却早已规划好未来的百年大计。面对年仅14.8万美元的销售额，公司总裁阿萨·坎德勒表示：\"我们从未放弃告诉全世界，可口可乐是世界上最好的健康与快乐饮料。\"虽然我认为\"健康\"这一说法还有待商榷，但我很高兴可口可乐在一百年后的今天，始终还遵循坎德勒当初立下的愿景。坎德勒又继续谈到：\"没有其他东西的味道能够像可乐一样深入人心。\"当年的可乐糖浆销售量不过只有11.6万加仑，时至今日，销售量已达到32亿加仑。",
    
    "I can't resist one more Candler quote: \"Beginning this year about March 1st . . . we employed ten traveling salesmen by means of which, with systematic correspondence from the office, we covered almost the territory of the Union.\" That's my kind of sales force.": 
        "我忍不住想要再引用坎德勒的另一段话：\"从今年三月开始，我们雇用了十位业务员，在与总公司保持密切联系下巡回各地推销产品，基本上我们的业务范围已涵盖整个美利坚合众国。\"这才是我心目中的销售力量。",
    
    "Companies such as Coca-Cola and Gillette might well be labeled \"The Inevitables.\" Forecasters may differ a bit in their predictions of exactly how much soft drink or shaving-equipment business these companies will be doing in ten or twenty years. Nor is our talk of inevitability meant to play down the vital work that these companies must continue to carry out, in such areas as manufacturing, distribution, packaging and product innovation. In the end, however, no sensible observer - not even these companies' most vigorous competitors, assuming they are assessing the matter honestly - questions that Coke and Gillette will dominate their fields worldwide for an investment lifetime. Indeed, their dominance will probably strengthen. Both companies have significantly expanded their already huge shares of market during the past ten years, and all signs point to their repeating that performance in the next decade.": 
        "像可口可乐和吉列这样的公司应该完全可以贴上\"注定成功\"的标签。分析师对于这些公司在未来10年或20年里究竟能卖多少软饮或剃须刀所做的预测可能会略有不同。而我们所说的\"注定成功\"并非贬低这些公司在生产、分销、包装和产品创新等领域继续开展的重要工作。然而，任何一个理性的观察者——即便是公司最强大的竞争对手，只要他们坦诚地看待问题——都不会怀疑，可口可乐和吉列在未来数十年内将在各自领域独领风骚。事实上，他们的优势可能还会加强。在过去十年中，这两家公司在其已经极大的市场份额基础上又显著扩大了份额，所有迹象都表明，在未来十年他们还会继续扩大。",
    
    "Obviously many companies in high-tech businesses or embryonic industries will grow much faster in percentage terms than will The Inevitables. But I would rather be certain of a good result than hopeful of a great one.": 
        "显然，许多高科技企业或新兴产业的公司，按照百分比计算的增速，比这些\"注定成功\"的公司快得多。但是，相比去期盼一个有可能的伟大结果，我宁愿得到一个确定的好结果。",
    
    "Of course, Charlie and I can identify only a few Inevitables, even after a lifetime of looking for them. Leadership alone provides no certainties: Witness the shocks some years back at General Motors, IBM and Sears, all of which had enjoyed long periods of seeming invincibility. Though some industries or lines of business exhibit characteristics that endow leaders with virtually insurmountable advantages, and that tend to establish Survival of the Fattest as almost a natural law, most do not. Thus, for every Inevitable, there are dozens of Impostors, companies now riding high but vulnerable to competitive attacks. Considering what it takes to be an Inevitable, Charlie and I recognize that we will never be able to come up with a Nifty Fifty or even a Twinkling Twenty. To the Inevitables in our portfolio, therefore, we add a few \"Highly Probables.\"": 
        "当然，即使查理和我终其一生追求永恒的持股，能够真正让我们找到的却属凤毛麟角。光是有市场领导地位并不足以保证成功，看看过去几年来通用汽车、IBM与西尔斯这些公司，都曾是领导一方的产业霸主，在所属的产业都被赋予其无可取代的优势地位，大者恒存的自然定律似乎牢不可破，但实际结果却不然。也因此，对于每一个\"注定成功\"的企业来说，还有许多\"假冒者\"——这些公司目前风光一时，但都禁不起竞争的攻击。考虑到要成为\"注定成功\"需要什么条件，查理和我认识到，我们永远不可能找出五十只\"必定赢\"甚至二十只\"闪亮二十\"的股票。因此，除了投资组合中的\"注定成功\"企业之外，我们还增加了一些\"极有可能成功\"的候选者。",
    
    "You can, of course, pay too much for even the best of businesses. The overpayment risk surfaces periodically and, in our opinion, may now be quite high for the purchasers of virtually all stocks, The Inevitables included. Investors making purchases in an overheated market need to recognize that it may often take an extended period for the value of even an outstanding company to catch up with the price they paid.": 
        "当然，即使你买的是最好的企业，也可能付出过高的成本。这种风险并非不存在，在我们看来，在当前的市场上，几乎所有股票的买家都面临着相当高的过高支付风险，包括那些\"注定成功\"的公司。在过热的股市中入市的投资者需要认识到，即使是一家卓越的公司，其价值可能也需要很长时间才能赶上他们所支付的价格。",
    
    "A far more serious problem occurs when the management of a great company gets sidetracked and neglects its wonderful base business while purchasing other businesses that are so-so or worse. When that happens, the suffering of investors is often prolonged. Unfortunately, that is precisely what transpired years ago at both Coke and Gillette. (Would you believe that a few decades back they were growing shrimp at Coke and exploring for oil at Gillette?) Loss of focus is what most worries Charlie and me when we contemplate investing in businesses that in general look outstanding. All too often, we've seen value stagnate in the presence of hubris or of boredom that caused the attention of managers to wander. That's not going to happen again at Coke and Gillette, however - not given their current and prospective managements.": 
        "一个更严重的问题是，当一家伟大公司的管理层分心并忽视了其良好的基础业务，转而收购那些平庸甚至更差的企业时，往往会导致投资者长期遭受痛苦。不幸的是，这正是多年前在可口可乐和吉列发生的事情。（你能想象几十年前，可口可乐养虾，吉列勘探石油吗？）当我们考虑投资那些整体看起来很出色的企业时，失去专注是最令查理和我担忧的问题。太多时候，我们看到价值在傲慢或无聊的干扰下停滞不前，管理者注意力分散。不过，好在可口可乐和吉列的现任和未来管理层都不会再犯这样的错误。",
    
    "Let me add a few thoughts about your own investments. Most investors, both institutional and individual, will find that the best way to own common stocks is through an index fund that charges minimal fees. Those following this path are sure to beat the net results (after fees and expenses) delivered by the great majority of investment professionals.": 
        "对于各位的个人投资，我可以提供一点心得供大家参考：大部分投资者，包括机构投资者和个人投资者，早晚会发现最好的投资股票方法，是购买管理费很低的指数基金。采用这种路径的人肯定会击败大多数投资专业人士提供的净结果（扣除费用和支出后）。",
    
    "Should you choose, however, to construct your own portfolio, there are a few thoughts worth remembering. Intelligent investing is not complex, though that is far from saying that it is easy. What an investor needs is the ability to correctly evaluate selected businesses. Note that word \"selected\": You don't have to be an expert on every company, or even many. You only have to be able to evaluate companies within your circle of competence. The size of that circle is not very important; knowing its boundaries, however, is vital.": 
        "不过，如果你选择建立自己的投资组合，此时有几个要点是需要你牢记的。聪明的投资并不复杂，尽管这远非易事。投资者真正需要的是正确评估所选企业的能力。注意\"所选\"这个词：你不必成为每家公司的专家，甚至许多公司都不需要。你只需要能够评估你能力圈范围内的公司。能力圈的大小并不重要；然而，知道它的边界在哪里才是至关重要的。",
    
    "To invest successfully, you need not understand beta, efficient markets, modern portfolio theory, option pricing or emerging markets. You may, in fact, be better off knowing nothing of these. That, of course, is not the prevailing view at most business schools, whose finance curriculum tends to be dominated by such subjects. In our view, though, investment students need only two well-taught courses - How to Value a Business, and How to Think About Market Prices.": 
        "要成功地投资，你不需要了解贝塔系数、有效市场理论、现代投资组合理论、期权定价或新兴市场。事实上，你可能更好的是对这些一无所知。当然，这并不是大多数商学院的主流观点，这些学校的金融课程往往被这些学科所主导。然而，在我们看来，投资学生只需要两门教得好的课程——如何评估企业价值，以及如何思考市场价格。",
    
    "Your goal as an investor should simply be to purchase, at a rational price, a part interest in an easily-understandable business whose earnings are virtually certain to be materially higher five, ten and twenty years from now. Over time, you will find only a few companies that meet these standards - so when you see one that qualifies, you should buy a meaningful amount of stock. You must also resist the temptation to stray from your guidelines: If you aren't willing to own a stock for ten years, don't even think about owning it for ten minutes. Put together a portfolio of companies whose aggregate earnings march upward over the years, and so also will the portfolio's market value.": 
        "作为投资者，你的目标应当仅仅是找到一个你能理解的、在未来5年、10年和20年内其收益肯定会大幅增长的公司部分股权。随着时间的推移，你会发现只有少数几家公司符合这些标准——所以当你发现一家符合条件的公司时，你应该买入相当数量的股票。你还必须抵制让你偏离指导方针的诱惑：如果你不愿意持有一只股票十年，那就不要连十分钟都持有。把这些总收益逐年上升的公司组合在一起，你投资组合的市值自然也会上升。",
    
    "Though it's seldom recognized, this is the exact approach that has produced gains for Berkshire shareholders: Our look-through earnings have grown at a good clip over the years, and our stock price has risen correspondingly. Had those gains in earnings not materialized, there would have been little increase in Berkshire's value.": 
        "虽然这很少被认识到，但这正是为伯克希尔的股东带来收益的精确方法：我们的透视盈余在过去几年间大幅跃进，而同期间我们的股票价格也跟着大涨。要不是我们的盈余大幅增加，伯克希尔所代表的价值就不可能大幅增长。",
    
    "The greatly enlarged earnings base we now enjoy will inevitably cause our future gains to lag those of the past. We will continue, however, to push in the directions we always have. We will try to build earnings by running our present businesses well - a job made easy because of the extraordinary talents of our operating managers - and by purchasing other businesses, in whole or in part, that are not likely to be roiled by change and that possess important competitive advantages.": 
        "我们现在拥有的庞大的收益基础，将不可避免地导致我们未来的收益增长落后于过去。但是，我们会继续朝着一贯的方向努力。我们将通过良好地经营现有业务来增加收益——这是一项因我们的运营经理人才华横溢而变得容易的工作——并通过收购其他不会因变革而动荡、且拥有重要竞争优势的业务来增加收益，无论是全部还是部分收购。",
    
    "USAir": "美国航空投资案",
    
    "When Richard Branson, the wealthy owner of Virgin Atlantic Airways, was asked how to become a millionaire, he had a quick answer: \"There's really nothing to it. Start as a billionaire and then buy an airline.\" Unwilling to accept Branson's proposition on faith, your Chairman decided in 1989 to test it by investing $358 million in a 9.25% preferred stock of USAir.": 
        "当维珍大西洋航空公司的总裁理查德·布兰森被问到如何成为百万富翁时，他的回答很简单：其实也没有什么！首先你要先成为一个亿万富翁，然后再去买一家航空公司就成了！但由于各位的董事长——也就是我本人不信邪，所以我在1989年决定以3.58亿美元投资取得美国航空年利率9.25%的特别股。",
    
    "I liked and admired Ed Colodny, the company's then-CEO, and I still do. But my analysis of USAir's business was both superficial and wrong. I was so beguiled by the company's long history of profitable operations, and by the protection that ownership of a senior security seemingly offered me, that I overlooked the crucial point: USAir's revenues would increasingly feel the effects of an unregulated, fiercely-competitive market whereas its cost structure was a holdover from the days when regulation protected profits. These costs, if left unchecked, portended disaster, however reassuring the airline's past record might be. (If history supplied all of the answers, the Forbes 400 would consist of librarians.)": 
        "当时我非常欣赏并崇拜美国航空时任总裁埃德·科洛德尼，但我对航空业的分析研究实在过于肤浅且错误百出，我被该公司过去历年来的获利能力所蒙骗，同时过分相信特别股可以提供给我们在债权上的保护，以致于忽略了最关键的一点：那就是美国航空的营收受到毫无节制的激烈价格竞争而大幅下滑的同时，其成本结构却仍旧停留在从前管制时代的高档，这样的高成本结构若不能找到有效解决的办法，将成为灾难的前兆。",
    
    "To rationalize its costs, however, USAir needed major improvements in its labor contracts - and that's something most airlines have found it extraordinarily difficult to get, short of credibly threatening, or actually entering, bankruptcy. USAir was to be no exception. Immediately after we purchased our preferred stock, the imbalance between the company's costs and revenues began to grow explosively. In the 1990-1994 period, USAir lost an aggregate of $2.4 billion, a performance that totally wiped out the book equity of its common stock.": 
        "要让成本结构合理化，美国航空必须大幅修改劳资契约，不过这偏偏又是航空公司难以达成的罩门，除了公司真正面临倒闭的威胁或甚至是真的倒闭。而美国航空也不例外，就在我们投资该公司特别股不久之后，公司营收与支出的缺口突然开始大幅扩大，在1990年至1994年间，美国航空累计亏损了24亿美元，此举让公司普通股的股东权益几乎耗损殆尽。",
    
    "For much of this period, the company paid us our preferred dividends, but in 1994 payment was suspended. A bit later, with the situation looking particularly gloomy, we wrote down our investment by 75%, to $89.5 million. Thereafter, during much of 1995, I offered to sell our shares at 50% of face value. Fortunately, I was unsuccessful.": 
        "在这段期间内，美国航空还是继续支付特别股股利给我们，直到1994年才停止，也因此在不久后，由于对该公司前景展望不太乐观，我们决定将美国航空特别股投资的账面价值调减75%，只剩下8,950万美元，从而到了1995年，我甚至对外提出以面额50%的折价，打算出售这笔投资，所幸最后并没有成功出脱。",
    
    "Mixed in with my many mistakes at USAir was one thing I got right: Making our investment, we wrote into the preferred contract a somewhat unusual provision stipulating that \"penalty dividends\" - to run five percentage points over the prime rate - would be accrued on any arrearages. This meant that when our 9.25% dividend was omitted for two years, the unpaid amounts compounded at rates ranging between 13.25% and 14%.": 
        "幸运的是，在这桩投资的一连串错误中，我总算做对了一件事：投资时，我们在特别股投资合约当中，特地加了一项\"惩罚股息\"条款，也就是说万一该公司延迟支付股息的话，除原有欠款外，还必须外加依基本利率5%的利息，也就是说因为这两年我们没有收到9.25%的股息，所以以后美国航空必须就未支付的款项加计13.25%与14%的利息。",
    
    "Facing this penalty provision, USAir had every incentive to pay arrearages just as promptly as it could. And in the second half of 1996, when USAir turned profitable, it indeed began to pay, giving us $47.9 million. We owe Stephen Wolf, the company's CEO, a huge thank-you for extracting a performance from the airline that permitted this payment. Even so, USAir's performance has recently been helped significantly by an industry tailwind that may be cyclical in nature. The company still has basic cost problems that must be solved.": 
        "面对这样的惩罚条款将督促美国航空尽快清偿对我们的欠款，而等到1996年下半年美国航空开始转亏为盈时，他们果真开始清偿这笔合计4,790万美元的欠款，为此我们特别要感谢美国航空现任总裁Stephen Wolf，是他让这家落难的航空公司得以付出这笔钱，同时美国航空的表现也归因于航空业景气复苏，当然该公司还是有成本结构的问题有待解决。",
    
    "In any event, the prices of USAir's publicly-traded securities tell us that our preferred stock is now probably worth its par value of $358 million, give or take a little. In addition, we have over the years collected an aggregate of $240.5 million in dividends (including $30 million received in 1997).": 
        "不过不论如何，目前美国航空普通股的市价显示我们所持有特别股的价值应该回复到3.58亿美元的面额左右，另外不要忘了，这几年来我们还陆陆续续从该公司收到2.4亿美元的股息（包含1997年的3,000万美元在内）。",
    
    "Early in 1996, before any accrued dividends had been paid, I tried once more to unload our holdings - this time for about $335 million. You're lucky: I again failed in my attempt to snatch defeat from the jaws of victory.": 
        "在稍早1996年初，我们还尚未收到积欠的股息之前，我再度尝试以3.35亿美元把这笔投资卖掉，所幸这次的举动又没有成功，使得我们得以从胜利之神口中逃过失败的命运。",
    
    "In another context, a friend once asked me: \"If you're so rich, why aren't you smart?\" After reviewing my sorry performance with USAir, you may conclude he had a point.": 
        "在另外一个场合，有一位朋友问我：\"你很有钱，可是为什么还这么笨？\"在进一步检讨本人在美国航空这个案子上的表现后，你可能会觉得他说得很有道理。",
    
    "Financings": "财务融资",
    
    "We wrote four checks to Salomon Brothers last year and in each case were delighted with the work for which we were paying. I've already described one transaction: the FlightSafety purchase in which Salomon was the initiating investment banker. In a second deal, the firm placed a small debt offering for our finance subsidiary.": 
        "去年我们总共四次向所罗门兄弟公司支付费用，令人高兴的是，每一张支票都对应着他们提供的优质服务。先前我已经说明过其中的一项交易——那就是买进国际飞安公司的交易，所罗门担任这项交易的投资银行顾问。第二个案子是所罗门帮我们旗下的财务子公司安排了一项融资案。",
    
    "Additionally, we made two good-sized offerings through Salomon, both with interesting aspects. The first was our sale in May of 517,500 shares of Class B Common, which generated net proceeds of $565 million. As I have told you before, we made this sale in response to the threatened creation of unit trusts that would have marketed themselves as Berkshire look-alikes. In the process, they would have used our past, and definitely nonrepeatable, record to entice naive small investors and would have charged these innocents high fees and commissions.": 
        "此外，透过所罗门我们完成另外两件案子，两者也都有相当有趣的特点，一件是在五月我们发行了517,500股的B级股，总共募得5.65亿美元的资金，关于这件案子，先前我就已经做过相关的说明，主要是因应坊间有些模仿伯克希尔的基金，避免他们以伯克希尔过去傲人的绩效记录对外吸引一些不知情的小额投资人，在收取高昂的手续费与佣金之后，却无法提供给投资人一个令人满意的投资结果。",
    
    "I think it would have been quite easy for such trusts to have sold many billions of dollars worth of units, and I also believe that early marketing successes by these trusts would have led to the formation of others. (In the securities business, whatever can be sold will be sold.) The trusts would have meanwhile indiscriminately poured the proceeds of their offerings into a supply of Berkshire shares that is fixed and limited. The likely result: a speculative bubble in our stock. For at least a time, the price jump would have been self-validating, in that it would have pulled new waves of naive and impressionable investors into the trusts and set off still more buying of Berkshire shares.": 
        "我相信这些仿伯克希尔基金可以很容易募得大笔的资金，而我也认为在这些基金成功募集到资金之后，一定还会有更多的基金跟进打着我们的旗号对外吸收资金，在证券业，没有什么是卖不掉的东西，而这些基金无可避免的会将所募得的资金大举投入到伯克希尔现有少数的股票投资组合，最后的结果很可能是伯克希尔本身以及其概念股股价暴涨而泡沫化，然后股价的上涨很可能又会吸引新一波的无知且敏感的投资人蜂拥投入这些基金，造成进一步的恶性循环。",
    
    "Some Berkshire shareholders choosing to exit might have found that outcome ideal, since they could have profited at the expense of the buyers entering with false hopes. Continuing shareholders, however, would have suffered once reality set in, for at that point Berkshire would have been burdened with both hundreds of thousands of unhappy, indirect owners (trustholders, that is) and a stained reputation.": 
        "有些伯克希尔的股东可能会发现这是一个大好的机会，因为可以利用新加入者不当的预期而想要趁机出脱持股赚取额外的利益，但在此同时选择继续留下来的股东却必须承担后来的苦果，因为等到回归现实后，我们会发现伯克希尔会有一群成千上万高档套牢的间接股东（亦即基金投资人），以及受到毁损的企业清誉。",
    
    "Our issuance of the B shares not only arrested the sale of the trusts, but provided a low-cost way for people to invest in Berkshire if they still wished to after hearing the warnings we issued. To blunt the enthusiasm that brokers normally have for pushing new issues - because that's where the money is - we arranged for our offering to carry a commission of only 1.5%, the lowest payoff that we have ever seen in a common stock underwriting. Additionally, we made the amount of the offering open-ended, thereby repelling the typical IPO buyer who looks for a short-term price spurt arising from a combination of hype and scarcity.": 
        "我们发行B级普通股不仅阻止了这些基金的销售，同时也让那些在听取我们的警告后仍希望投资伯克希尔的人能够以低成本的方式进场。为了抑制经纪商对于推销新股 normally 所展现的高度热情——因为这是他们获利的主要来源——我们特别将这次发行的佣金费率压低到只有1.5%，这是我有史以来所见过股票承销案中最低的佣金费率，同时我们还让这次发行保持开放空间的形态，从而吓退那些只想短线炒作获取暴利的典型IPO买家。",
}

print(f"翻译库共有 {len(TRANSLATIONS)} 个条目")

# 构建查找表，包含各种变体
def build_lookup_table():
    lookup = {}
    for key, value in TRANSLATIONS.items():
        # 原始键
        lookup[key] = value
        # 去除开头星号和空格
        if key.startswith('* '):
            lookup[key[2:]] = value
        # 去除末尾标点
        for punc in [':', '.', ',', ';', '!', '?']:
            if key.endswith(punc):
                lookup[key[:-1]] = value
                if key.startswith('* '):
                    lookup[key[2:-1]] = value
    return lookup

TRANSLATION_LOOKUP = build_lookup_table()
print(f"查找表共有 {len(TRANSLATION_LOOKUP)} 个条目")

def normalize_text(text):
    """标准化文本用于匹配"""
    # 去除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def find_translation(en_clean):
    """根据英文文本找到最佳翻译"""
    
    # 精确匹配
    if en_clean in TRANSLATION_LOOKUP:
        return TRANSLATION_LOOKUP[en_clean]
    
    # 去除开头的星号和空格
    en_no_star = en_clean.lstrip('* ')
    if en_no_star in TRANSLATION_LOOKUP:
        return TRANSLATION_LOOKUP[en_no_star]
    
    # 去除末尾标点后匹配
    for punc in [':', '.', ',', ';', '!', '?']:
        if en_clean.endswith(punc):
            en_trimmed = en_clean[:-1]
            if en_trimmed in TRANSLATION_LOOKUP:
                return TRANSLATION_LOOKUP[en_trimmed]
            en_no_star_trimmed = en_no_star[:-1] if en_no_star.endswith(punc) else en_no_star
            if en_no_star_trimmed in TRANSLATION_LOOKUP:
                return TRANSLATION_LOOKUP[en_no_star_trimmed]
    
    # 开头匹配（前150字符）
    en_norm = normalize_text(en_clean)[:150].lower()
    for key, value in TRANSLATIONS.items():
        key_norm = normalize_text(key)[:150].lower()
        if key_norm == en_norm:
            return value
    
    return None

# 测试匹配
print("\n测试翻译匹配：")
test_texts = [
    "To the Shareholders of Berkshire Hathaway Inc.:",
    "* Each Class B share has an economic interest equal to 1/30th of that possessed by a Class A share",
    "Our gain in net worth during 1996 was $6.2 billion",
]

for t in test_texts:
    result = find_translation(t)
    print(f"  匹配 '{t[:50]}...': {'✓' if result else '✗'}")
