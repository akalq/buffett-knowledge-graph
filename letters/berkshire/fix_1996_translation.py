#!/usr/bin/env python3
"""
修复1996年巴菲特致股东信的中文翻译质量
- 分析双语块，找出中文长度不足英文50%的块
- 使用参考翻译补全
"""

import re
import json
from pathlib import Path

# 读取原始HTML文件
html_path = Path("./投资研究/知识库/巴菲特知识库-LearnBuffett版/letters/berkshire/1996.html")
html_content = html_path.read_text(encoding='utf-8')

# 从格隆汇获取的完整翻译 - 这是一个关键段落的参考翻译
# 我们将用它来补全缺失的翻译
REFERENCE_TRANSLATIONS = {
    # 第一部分: 内在价值表格相关
    "From the table tell you, our investments per share increased in 1996 by": 
        "从表格可见，1996年我们的每股投资金额增长了29%，而非投资业务的经营收益更是增长了63.2%。我们的目标是让这两项数据以合理速度稳定增长，若能偶尔实现超预期的爆发式增长自然更佳。不过，这样的预期会受到两项现实因素制约：首先，我们很难再达到或接近过去的高增长率，核心原因是伯克希尔当前的资本规模已十分庞大——事实上，公司资本体量已跻身全美企业前十，过多资本必然会影响整体回报率；其次，无论增长速度如何，都难以保持绝对平稳：第一栏数据易随股市波动而起伏，第二栏数据则会因巨灾再保险业务的盈利波动而变化。",
    
    "In the table, the donations made pursuant to our shareholder-designated contributions program are charged against the second column":
        "表格中，股东指定捐赠款项被列为第二栏的减项——尽管我们将其视为股东福利而非企业支出，但企业其他开支同样计入第二栏扣除。值得一提的是，我们的企业开支远低于美国大企业平均水平，总部每年的税后费用占账面价值的比率不足万分之二。即便如此，查理仍觉得这一比率过高，我想主要该归咎于我使用的伯克希尔企业专机"无可辩解号"。不过，自从我们收购了专注飞行训练的飞安国际后，查理对飞机的态度来了个180度大转变，如今只要谈及飞机就兴致勃勃。",
    
    "Seriously, costs matter":
        "认真来说，成本控制至关重要。举例而言，许多共同基金每年的经营费用约占资产规模的1%，这相当于间接侵蚀了投资人近10%的投资回报。查理和我不敢向各位保证伯克希尔的投资绩效，但我们向各位承诺，伯克希尔赚到的每一分钱都会原原本本地落入股东口袋。我们是来帮各位赚钱的，而不是来从各位身上捞钱的。",
    
    # 堪萨斯银行家保险收购故事
    "You might be interested in the carefully-crafted and sophisticated acquisition strategy that allowed Berkshire to nab this deal":
        "大家或许会对我们这次精心设计的购并计划感到兴趣，在1996年初我受邀参加侄媳妇Jane40岁的生日宴会，由于我个人对于社交活动通常不太感兴趣，所以很自然地我按照惯例想出许多理由以婉拒这项邀请，不过对方显然有备而来，特别将我安排在另外一位我极有兴趣打交道的对象Roy Dinsdale（Jane的父亲）的旁边，此举使得我无法拒绝而欣然赴会。",
    
    "The party took place on January 26":
        "生日宴会在1月26日举行，虽然当时现场音乐震耳欲聋（我实在搞不懂为何乐队总是要弹得那么大声，难道他们的出场费是按照分贝数计算的吗？），不过我还是听到Roy说他刚参加完堪萨斯银行家保险的董事会，这是我一直相当欣赏的一家公司，我大声地响应他说，如果这家公司有意出售的话，记得一定要通知我。",
    
    "On February 12, I got the following letter":
        "2月12日我收到一封Roy的来函，上面写到：亲爱的沃伦，随函附送一份堪萨斯银行家保险的年度财务报表，就是上次在Jane的生日宴会上提到的那一家公司，如果你有任何需要，请务必让我知道。2月13日，我告诉Roy愿意出7,500万美元买下这家公司，不久之后，整个交易就搞定，现在的我正盘算明年还要再参加Jane的生日宴会。",
    
    "Fortunately, Richard had also been a long-time shareholder of FlightSafety":
        "碰巧的是，Richard同时也是国际飞安公司长期投资的股东，刚好在去年他认为这两家公司应该有机会可以做一个结合，他相当了解伯克希尔购并公司的标准，同时也知道国际飞安79岁的总裁Al Ueltschi想要为自己的公司找一个理想的归宿，好为自己的股权找到一层保障，所以就在七月份，Richard写信给所罗门公司的总裁Bob Denham请他研究这项合并交易的可能性。",
    
    "Bob took it from there":
        "Bob于是接手进行这个案子，在9月18日我和Al正式在纽约碰面，我对国际飞安这家公司的经营状况本来就相当熟悉，而在60秒内我马上就知道Al正是符合我们类型的经理人，一个月后，合约正式敲定，由于查理跟我希望能够尽量避免再发行伯克希尔的新股份，所以在这项交易中，虽然我们提供国际飞安原股东换取股票或现金两种选择，但是交易条件等于间接鼓励这些税负没有太大差异的股东选择领取现金，结果总计最后有51%股份领取现金，41%换得伯克希尔A级普通股，另外8%换得伯克希尔B级普通股。",
    
    "Al has had a lifelong love affair with aviation":
        "Al一生热爱飞行，曾经驾驶过查理林登号，在经过1930年代轰轰烈烈的飞行事业之后，他开始担任泛美航空的机长，之后在1951年创立国际飞安公司，将这家公司塑造成飞行仿真器制造与飞行员训练的世界级领导公司（单引擎、直升机、客机与水上飞机），营业据点遍布41个地方，拥有175座的飞行仿真器，大至波音747客机，小到Cessna 210型小飞机，大家要知道飞行仿真器的造价可不便宜，有的要价甚至高达1,900万美金，所以这一行不像我们原来拥有的其它事业，算是相当资本密集的，该公司大约有一半的营业收入来自于训练飞行员的收入，其余则来自于航空公司与军事单位。",
    
    "An observer might conclude from our hiring practices":
        "有人可能会怀疑我们现在雇用人的政策，可能是缘于早期年龄歧视政策所受到的创伤，其实真正的原因乃是出于自私的观点，因为我们认为实在是很难教新狗老把戏！在伯克希尔，许多经理人虽然已经年过70，但是他们还是像年轻时一样活跃，频频击出全垒打，所以如果各位有意到本公司谋得一职，请记得运用一位高龄76岁老翁如何追到25岁年轻辣妹的技巧，当同年龄的同伴很钦羡地问他：你到底是如何说服对方同意的呢？他回答到：很简单，我告诉她我今年86岁！",
    
    # 保险业务
    "As in the past three years, we once again stress that the good results we are reporting for Berkshire stem in part from our super-cat business having a lucky year":
        "与过去三年一样，我们再次强调今年伯克希尔保险事业之所以能够有这么好的成绩，部分的原因要归功于霹雳猫业务又渡过幸运的一年，从事这类业务，我们出售保单给保险公司与再保公司以分散其面临超大型意外灾害所可能承担的风险，由于真正重大的灾害并不常发生，所以我们的霹雳猫业务有可能在连续几年赚大钱后，才突然发生重大的损失，换句话说，我们这项霹雳猫业务到底有多吸引人可能要花上好几年才有办法看得清，不过大家必须明了，所谓的重大损失的年头不是可能会发生，而是肯定会发生，唯一的问题是它什么时候会降临。",
    
    "I emphasize this lugubrious point because I would not want you to panic and sell your Berkshire stock upon hearing that some large catastrophe had cost us a significant amount":
        "我之所以会把丑话说在前头，是因为我不希望大家那天突然听到伯克希尔因为某某大型意外灾害须理赔一大笔钱时，恐慌地拋售手中的持股，而如果届时你真的会有这种反应，那么你根本就不应该拥有本公司的股份，就像是如果你是那种碰到股市崩盘，会恐慌性的拋售手中股票的人，我建议你最好不要投资股票，听到坏消息而把手中的好股票卖掉通常不会是一个明智的决定。（数十年前创办可口可乐的天才企业家Robert Woodruff曾经被问到，什么情况下是出售可口可乐股票的好时机，Woodruff简短的回答到，我不知道，我从来就没有卖过！）。",
    
    "In our super-cat operation, our customers are insurers that are exposed to major earnings volatility":
        "谈到霹雳猫保险业务，我们的客户主要是一些想要降低本身必须承担盈余变动剧烈风险的保险公司，而我们贩卖的产品——当然一定要以合理的价格，将这些盈余变动的风险转移到本公司的账上，因为我们对于伯克希尔公司盈余剧烈的变动一点都不会介意，查理跟我宁可接受上下变动但平均可达15%的结果，也不要平稳的12%。（就像是我们知道公司的盈余每天、每周都会变动，那么我们又何必强求公司的盈余变化一定要跟地球环绕太阳轨道的时间一致呢？）我想如果伯克希尔的股东合伙人也能有这样的看法，那么我们执行业务时便能更得心应手，而这也是为什么我们要一再提出相同警告的原因。",
    
    "We took on some major super-cat exposures during 1996":
        "我们在1996年陆续接了好几件大业务，在年中我们与全美保险签约承保佛罗里达飓风险，虽然没有确切的资料可供左证，但我们相信这应该是单一公司独力承受单一风险的最高记录，接着到年底，我们又与加州地震局签约承保比佛罗里达飓风高出一倍的理赔上限，保单预计从1997年4月1日开始生效，再一次我们独立承揽所有的风险，虽然承保的金额相当庞大，但是即使在最坏的状况下，任何一件大型灾害的税后损失也不会超过六亿美元，大约不到伯克希尔净值的3%或市值的1.5%，大家要了解这类风险的影响性，比起股票市场变动对我们的影响性来说，前者可谓是小巫见大巫。",
    
    "In the super-cat business, we have three major competitive advantages":
        "在霹雳猫保险业务，我们主要有三项竞争优势，首先向我们投保再保险的客户都知道我们有能力，也会在最糟糕的情况下履约付款，因为万一真的发生什么大的灾难，很难保证金融恐慌就不会接踵而至，届时在其客户最需要援助时，可能连一些原本享有盛誉的再保公司都拿不出钱来，而事实上我们之所以从来不将风险再转嫁出去的一个原因也是因为我们对于灾难发生时，其它保险公司能否顺利支付赔款的能力有所保留，反之只要是伯克希尔做出的保证，所有的保户都可以百分之百确定一定可以立即得到理赔。",
    
    "Even if perfection in assessing risks is unattainable":
        "虽然保险业者无法准确地评估风险到底有多大，不过我们却还是可以合理的接下保单，就像是你并不一定要真的知道一个人的实际年龄，才能判断他是否可以去投票或是一定要知道一个人几公斤重才认为他该不该减肥。同样的，从事保险这一行，大家必须谨记的是，基本上所有的意外都不会让人感到愉快，所以在接下保单时，我们心里早有预备，准备把90%的保费收入花在损失理赔与相关费用之上，慢慢的一段时间下来，我们就会发现，这样的订价是否合理，这绝对需要时间来证明，霹雳猫保险这一行就像是投资事业一样，绝对需要一段很长的时间，你才能确切的知道自己到底在干什么。",
    
    "What I can state with certainty, however, is that we have the best person in the world to run our super-cat business":
        "不过有一点我绝对可以向各位保证，我们拥有全世界最优秀的霹雳猫保险专家，那就是Ajit Jain，他在伯克希尔的价值大到难以想象，在再保险这一行，恐怖的灾难时常发生，我很清楚的原因是我个人在1970年代就抱了不少个地雷，而盖可在1980年代初期，即使当时拥有最能干的经理人，也同样签了一堆愚蠢的保险合约，不过提到Ajit，我可以向各位保证，绝对不会再犯同样的错误。",
    
    "I have mentioned that a mega-catastrophe might cause a catastrophe in the financial markets":
        "不过另一方面我也说过，自然灾害的发生同样也会间接导致金融风暴的发生，这样的可能性不大，但也不是不可能，要是加州真的发生规模大到我们理赔上限的大地震，我们旗下其它事业也可能会受到严重的打击，比如说喜诗糖果、富国银行或房利美等，不过总的来说，我们应该可以妥善处理发生的状况。就这方面而言，我们试着事先规划伯克希尔的未来，时时谨记查理常说的一句格言："希望能够知道自己最后会死在哪里，然后打死都不去那里！"（事先回想真的有效，大家可以试着多唱唱以前流行的乡村歌曲，很快的你就会发现重新找回了你的房子、你的车子跟老婆），如果我们没办法承担可能的后果，不管其可能性有多小，那么我们就必须避免播下罪恶的种子。",
    
    # GEICO相关
    "There's nothing esoteric about GEICO's success":
        "GEICO的成功并不神秘：该公司的竞争力直接源于其作为低成本经营者的地位。低成本带来低价格，低价格吸引并留住优秀的投保人。一旦这种良性循环运转起来，政策持有人就会向朋友推荐我们。GEICO每年获得超过一百万次的转介绍，而这些转介绍客户贡献了超过一半的新业务，这种优势为我们节省了大量的获客成本——而这也使得我们的成本进一步降低。",
    
    "This formula worked in spades for GEICO in 1996":
        "这个公式在1996年对GEICO产生了极佳的效果：其自愿汽车保单数量增长了10%。在此之前的20年里，该公司最好的年度增长率仅为8%，而且只达到过一次。更重要的是，增长率在全年都在加速，其中在非标准市场领域取得了重大进展，而这正是GEICO过去开发不足的领域。我在这里关注自愿保单的原因在于，我们从分配风险池等渠道获得的非自愿业务是亏损的，因此这类业务的增长是最不受欢迎的。",
    
    "We expect new competitors to enter the direct-response market":
        "我们预计会有新的竞争对手进入直复营销市场，我们现有的一些竞争对手也可能进行地域扩张。尽管如此，我们所享有的规模经济应该能够让我们保持甚至扩大围绕经济城堡的护城河。在我们拥有较高市场渗透率的地区，我们在成本方面做得最好。随着我们的保单数量增长，同时渗透率也随之提高，我们预计成本将大幅降低。GEICO可持续的成本优势，正是1951年吸引我投资这家公司的原因，当时整个公司的估值仅为700万美元。这也是为什么我觉得伯克希尔应该在去年为剩余49%的股权支付23亿美元的原因。",
    
    "Maximizing the results of a wonderful business requires management and focus":
        "想要让一家好公司的表现发挥到极致，必须依赖优秀的管理人员与明确的目标方向。很幸运的是，我们有Tony这样一位杰出的管理者，他对企业专注从未动摇。为了让整个GEICO组织像他一样专注，我们需要一个本身高度聚焦的薪酬计划——在我们的收购完成后，我们立即推出了这样一个计划。",
    
    "The GEICO plan exemplifies Berkshire's incentive compensation principles":
        "GEICO这项计划充分说明了伯克希尔薪资奖励的原则，那就是必须要能够达到以下目标：（1）根据具体运营业务的经济特性量身定制；（2）简单明了，便于衡量目标的实现程度；以及（3）与计划参与者的日常活动直接相关。作为推论，我们回避类似彩票的安排，比如伯克希尔股票的期权，其最终价值——可能从零到巨额不等——完全不在我们希望影响其行为的人的控制之下。在我们看来，一种产生不稳定回报的制度不仅对所有者是浪费的，而且可能实际上会抑制我们在管理者身上所珍视的专注行为。",
    
    "Lou Simpson continues to manage GEICO's money in an outstanding manner":
        "Lou Simpson继续出色地管理着GEICO的资金：去年，他管理的股票投资组合比标准普尔500指数高出了6.2个百分点。在Lou负责的GEICO业务领域，我们仍然将薪酬与业绩挂钩——但是与四年期内的投资业绩挂钩，而非与承保业绩或GEICO整体业绩挂钩。我们认为，让保险公司支付与整体公司业绩挂钩的奖金是愚蠢的，因为在一个业务领域——无论是承保还是投资——的出色工作，可能会被另一个领域的糟糕表现完全抵消。如果你在伯克希尔的击球率达到.350，你可以确信你会得到与之相称的报酬，即使团队其他人的击球率仅为.200。然而，幸运的是，在Lou和Tony这两位关键职位上，我们都拥有名人堂级别的选手。",
    
    "Though they are, of course, smaller than GEICO, our other primary insurance operations turned in equally stunning results last year":
        "虽然比起GEICO，我们其它主要保险事业规模要小得多，但他们在去年同样缴出惊人的成绩单。国家险的的传统业务综合成本率为74.2，与往常一样，与保费规模相比，产生了大量的浮存金。在过去三年中，由Don Wurster运营的这一业务板块，平均综合成本率为83.0。我们的homestate业务，由Rod Eldred管理，即使吸收了新州扩张的费用，仍录得87.1的综合成本率。Rod的三年综合成本率为惊人的83.2。伯克希尔的工伤险业务，由加州的Brad Kinstler负责，现已扩展到其他六个州，尽管扩张成本不菲，但再次取得了优异的承保利润。最后，Central States Indemnity的John Kizer，在保费规模创历史新高的同时，也取得了良好的承保收益。总体而言，我们较小的保险业务（现在包括堪萨斯银行家担保公司）的承保记录几乎在行业中无与伦比。Don、Rod、Brad和John都为伯克希尔创造了重大价值，我们相信未来还会有更多贡献。",
    
    # 透视收益
    "The following table sets forth our 1996 look-through earnings":
        "下表列出了1996年的透视收益，不过我需要提醒大家，这些数字只是近似值，因为它们基于多项主观判断。（被投资公司支付给我们的股息已包含在第12页所列的经营收益项目中，大部分在"保险集团：净投资收益"项下。）",
    
    # 股票投资
    "Inactivity strikes us as intelligent behavior":
        "我们觉得持仓不动是明智的行为。我们和大多数企业经理一样，不会因为市场预测美联储贴现率的小幅波动，或是因为某些华尔街权威人士改变了对市场的看法，就狂热地买卖利润丰厚的下属子公司。那么，我们为什么要以不同的方式对待自己持有的优秀公司少数股权呢？上市公司投资的成功之道与并购子公司的成功之道并没有什么不同。在两种情况下，你都需要只是以合理的价格买进一家拥有优秀经济特性和诚实能干的管理层的企业。此后，你只需留意这些特质是否仍然存在。",
    
    "When carried out capably, an investment strategy of that type will often result in its practitioner owning a few securities":
        "如果执行得当，这种投资策略通常会导致投资者持有少数几种证券，而这些证券将占据其投资组合的很大一部分。这位投资者如果采取购买一批杰出大学篮球明星未来收入20%权益的策略，也会得到类似的结果。其中少数人后来成为了NBA的明星，投资者从他们身上获得的收益很快就成为他投资王国的主要"税收"收入。建议这位投资者仅仅因为最成功的投资已经占据投资组合的主导地位就卖出部分持仓，这种建议就好比建议公牛队交易迈克尔·乔丹，因为他对球队已经变得太过重要。",
    
    "Obviously all businesses change to some extent":
        "当然，任何企业或多或少都会发生改变。今天，喜诗糖果在许多方面都与1972年我们收购它时不同：如今它生产不同种类的糖果，使用不同的机器，并通过不同的分销渠道销售。但今天人们购买盒装巧克力的原因，以及他们从我们这里而不是从别人那里购买的原因，与上世纪20年代喜诗家族创办企业时几乎没有改变。此外，这些购买动机在未来20年甚至50年内也不太可能改变。",
    
    "We look for similar predictability in marketable securities":
        "我们在有价证券投资中寻找类似的可预测性。以可口可乐为例：在罗伯托·古崔塔的领导下，可口可乐产品的销售热情和想象力都大大增强，他在为股东创造价值方面做得非常出色。在Don Keough与Doug Ivester的协助之下，古崔塔从头到尾重新塑造了公司的每一个方面。但是，这项业务的基础——支撑可口可乐竞争主导地位和经济优势的品质——这些年来一直保持不变。",
    
    "I was recently studying the 1896 report of Coke":
        "最近我正在研读可口可乐1896年的年报（所以大家现在看我们的年报应该还不嫌太晚）。虽然当时可口可乐已经成为冷饮市场的领导者，但那也不过只有十年的光景。然而在当时，该公司却早已规划好未来的百年大计。面对年仅14.8万美元的销售额，公司总裁阿萨·坎德勒表示："我们从未放弃告诉全世界，可口可乐是世界上最好的健康与快乐饮料。"虽然我认为"健康"这一说法还有待商榷，但我很高兴可口可乐在一百年后的今天，始终还遵循坎德勒当初立下的愿景。坎德勒又继续谈到："没有其他东西的味道能够像可乐一样深入人心。"当年的可乐糖浆销售量不过只有11.6万加仑，时至今日，销售量已达到32亿加仑。",
    
    "I can't resist one more Candler quote":
        "我忍不住想要再引用坎德勒的另一段话："从今年三月开始，我们雇用了十位业务员，在与总公司保持密切联系下巡回各地推销产品，基本上我们的业务范围已涵盖整个美利坚合众国。"这才是我心目中的销售力量。",
    
    "Companies such as Coca-Cola and Gillette might well be labeled \"The Inevitables\"":
        "像可口可乐和吉列这样的公司应该完全可以贴上"注定成功"的标签。分析师对于这些公司在未来10年或20年里究竟能卖多少软饮或剃须刀所做的预测可能会略有不同。而我们所说的"注定成功"并非贬低这些公司在生产、分销、包装和产品创新等领域继续开展的重要工作。然而，任何一个理性的观察者——即便是公司最强大的竞争对手，只要他们坦诚地看待问题——都不会怀疑，可口可乐和吉列在未来数十年内将在各自领域独领风骚。事实上，他们的优势可能还会加强。在过去十年中，这两家公司在其已经极大的市场份额基础上又显著扩大了份额，所有迹象都表明，在未来十年他们还会继续扩大。",
    
    "Of course, Charlie and I can identify only a few Inevitables":
        "当然，即使查理和我终其一生追求永恒的持股，能够真正让我们找到的却属凤毛麟角。光是有市场领导地位并不足以保证成功，看看过去几年来通用汽车、IBM与西尔斯这些公司，都曾是领导一方的产业霸主，在所属的产业都被赋予其无可取代的优势地位，大者恒存的自然定律似乎牢不可破，但实际结果却不然。也因此，对于每一个"注定成功"的企业来说，还有许多"假冒者"——这些公司目前风光一时，但都禁不起竞争的攻击。考虑到要成为"注定成功"需要什么条件，查理和我认识到，我们永远不可能找出五十只"必定赢"甚至二十只"闪亮二十"的股票。因此，除了投资组合中的"注定成功"企业之外，我们还增加了一些"极有可能成功"的候选者。",
    
    "You can, of course, pay too much for even the best of businesses":
        "当然，即使你买的是最好的企业，也可能付出过高的成本。这种风险并非不存在，在我们看来，在当前的市场上，几乎所有股票的买家都面临着相当高的过高支付风险，包括那些"注定成功"的公司。在过热的股市中入市的投资者需要认识到，即使是一家卓越的公司，其价值可能也需要很长时间才能赶上他们所支付的价格。",
    
    # 美国航空
    "I liked and admired Ed Colodny, the company's then-CEO":
        "当时我相当喜爱同时也崇拜美国航空当时的总裁Ed Colodny，直到现在仍是如此，不过我对于美国航空业的分析研究实在是过于肤浅且错误百出，我被该公司过去历年来的获利能力所蒙骗，同时过分相信特别股可以提供给我们在债权上的保护，以致于忽略了最关键的一点：那就是这样美国航空的营收受到毫无节制的激烈价格竞争而大幅下滑的同时，其成本结构却仍旧停留在从前管制时代的高档，这样的高成本结构若不能找到有效解决的办法，将成为灾难的前兆。",
    
    "To rationalize its costs, however, USAir needed major improvements in its labor contracts":
        "要让成本结构合理化，美国航空必须大幅修改其劳资契约，不过这偏偏又是航空公司难以达成的罩门，除了公司真正面临倒闭的威胁或甚至是真的倒闭。而美国航空也不例外，就在我们投资该公司特别股不久之后，公司营收与支出的缺口突然开始大幅扩大，在1990年至1994年间，美国航空累计亏损了24亿美元，此举让公司普通股的股东权益几乎耗损殆尽。",
    
    "For much of this period, the company paid us our preferred dividends":
        "在这段期间内，美国航空还是继续支付特别股股利给我们，直到1994年才停止，也因此在不久后，由于对该公司前景展望不太乐观，我们决定将美国航空特别股投资的账面价值调减75%，只剩下8,950万美元，从而到了1995年，我甚至对外提出以面额50%的折价，打算出售这笔投资，所幸最后并没有成功出脱。",
    
    "In any event, the prices of USAir's publicly-traded securities tell us that our preferred stock is now probably worth its par value":
        "不过不论如何，目前美国航空普通股的市价显示我们所持有特别股的价值应该回复到3.58亿美元的面额左右，另外不要忘了，这几年来我们还陆陆续续从该公司收到2.4亿美元的股息（包含1997年的3,000万美元在内）。",
    
    # 所罗门融资
    "Additionally, we made two good-sized offerings through Salomon":
        "此外，透过所罗门我们完成另外两件案子，两者也都有相当有趣的特点，一件是在五月我们发行了517,500股的B级股，总共募得5.65亿美元的资金，关于这件案子，先前我就已经做过相关的说明，主要是因应坊间有些模仿伯克希尔的基金，避免他们以伯克希尔过去傲人的绩效记录对外吸引一些不知情的小额投资人，在收取高昂的手续费与佣金之后，却无法提供给投资人一个令人满意的投资结果。",
    
    "I think it would have been quite easy for such trusts to have sold many billions of dollars worth of units":
        "我相信这些仿伯克希尔基金可以很容易募得大笔的资金，而我也认为在这些基金成功募集到资金之后，一定还会有更多的基金跟进打着我们的旗号对外吸收资金，在证券业，没有什么是卖不掉的东西，而这些基金无可避免的会将所募得的资金大举投入到伯克希尔现有少数的股票投资组合，最后的结果很可能是伯克希尔本身以及其概念股股价暴涨而泡沫化，然后股价的上涨很可能又会吸引新一波的无知且敏感的投资人蜂拥投入这些基金，造成进一步的恶性循环。",
    
    "Our issuance of the B shares not only arrested the sale of the trusts":
        "B级普通股的发行正可以抑止这些仿伯克希尔基金的销售，同时提供小额投资人投资伯克希尔的低成本管道，如果在他们听过我之前所提出的警告后仍执意要投资的话，而为了降低经纪人一般喜欢推销新股发行的习惯（因为这是真正有赚头的所在），我们刻意将承销佣金降到1.5%，这是所有发行新股承销佣金最低的比率，此外我们对发行新股的数量不设上限，以避免一些专门投资初次上市股票抢帽子的投机客，利用新股数量稀少而刻意炒作赚取短期股价飙涨的差价。",
    
    "Overall, we tried to make sure that the B stock would be purchased only by investors with a long-term perspective":
        "总而言之，我们希望买进B级普通股的投资人是真正希望长期投资的，事实证明我们的做法相当成功，在公开发行后的B级普通股成交量（亦即代表换手的情形）远低于一般初次上市的股票，结果总计我们因此新增了40,000名的股东，我相信他们大部分都了解他们到底在投资什么，同时与我们拥有相同的经营理念。",
    
    "Salomon could not have performed better in the handling of this unusual transaction":
        "在这次不常见的交易中，所罗门的表现好得不能再好了，身为我们的投资银行，他们充分了解我们想要达成的目标，从而量身订做，提供符合我们需要的服务，事实上若是按照一般的标准模式，所罗门应该可以赚进更多钱，有可能比现在多十倍以上，不过他们并没有刻意引导我们这样子去做，相反地有时他们还是提出一些对自己本身利益冲突，但却有助于伯克希尔达成目的的一些建议，感谢Terry这次为我们操刀所做的努力与贡献。",
    
    "Given that background, it won't surprise you to learn that we again went to Terry":
        "基于这样的背景，大家不难想象当伯克希尔决定发行以所持有的所罗门股份做为转换标的的可转换票券时，我们又再度找上Terry，再一次所罗门的表现一流，卖出以五年为期、总面额五亿美元的票券，共取得4.471亿美元的资金，每张面额1,000美元的票券可以转换成17.65股的所罗门股份，同时有权在三年后要求以账面价值卖回，总计原先票面折价加上1%的票面利息，此证券可以给予到期不选择转换成所罗门股份的投资人3%的报酬率，不过我想投资人在到期前选择不转换的机率微乎其微，若果真如此，在转换前我们实际负担的利率成本大约在1.1%左右。",
    
    "Though it was a close decision, Charlie and I have decided to enter the 20th Century":
        "虽然这个决定有点赶，查理跟我本人已决定正式跨入二十一世纪，我们决定从现在开始将在公司网络上公布每季与每年最新的伯克希尔年报，大家可以透过以下这个网址http://www.berkshirehathaway.com找到相关的讯息，我们会固定选在星期六把报告摆上去，主要的目的是希望大家能够有充足的时间在股市开盘做出进出的决定，预计未来一年内公布报告的时间为1997年5月17日、8月16日、11月15日以及1998年3月14日，同时网站上也会有我们对外发布的其它公开讯息。",
    
    "At some point, we may stop mailing our quarterly reports":
        "在此同时，我们也将停止过去邮寄每季季报的习惯，而直接将它们公布在公司网站上，此举不但可以大幅减少邮寄的成本，同时也因为我们有一些股东的股份是登记在别人的名下，这使得季报最后送到真正股东手上的时间很不一定，有的股东收到报告的时间整整比其它股东晚了好几个礼拜。",
    
    "The drawback to Internet-only distribution is that many of our shareholders lack computers":
        "透过网络公布也有一个很大的缺点，那就是许多我们的股东从来不使用计算机，当然大家还是可以透过同事或朋友的帮助把它们给打印下来，如果大家觉得还是用寄比较好的话可以向我反应，我们很想听听大家的意见，至少在1997年还是会持续原来的做法，另外必须强调的是，每年的年报除了在网络上公布之外，依然还是会用邮寄的方式送到各位的手上。",
    
    "About 97.2% of all eligible shares participated in Berkshire's 1996 shareholder-designated contributions program":
        "大约有97.2%的有效股权参与1996年的股东指定捐赠计划，总计约1,330万美元捐出的款项分配给3,910家慈善机构，详细的名单参阅附录。每年都有一小部分的股东由于没有将股份登记在本人的名下，或是没能在60天的期限内，将指定捐赠的表格送回给我们，而没办法参加我们的指定捐赠计划，对此查理跟我感到相当头痛，不过我们必须忍痛将这些指定捐赠剔除，因为我们不可能在拒绝其它不符合规定股东的同时，还破例让这些人参与。",
    
    # 股东大会
    "Our capitalist's version of Woodstock":
        "资本家版的伍斯达克音乐会——伯克希尔股东年会将在五月五日星期一举行，查理跟我实在是很喜欢这场盛会，所以我们很希望大家都能来。会议预计从早上9点半正式开始，中午休息15分钟（现场备有餐点，不过必须付费），然后会继续与许多死忠的股东谈到下午三点半。去年全美50州都有股东代表出席，另外还有来自海外地区，如澳洲、希腊、以色列、葡萄牙、新加坡、瑞典、瑞士以及英国等国家。股东年会是公司股东可以得到有关公司经营所有问题解答的场合，所以查理跟我一定会竭尽所能地回答各位提出的问题，直到我们头昏脑胀为止（如果查理跟我有异状时，希望各位能及时发现）。",
    
    "Last year we had attendance of 5,000":
        "去年总共有5,000名股东与会，虽然我们预先另外准备了三间小会议室，不过还是把当时的会场Holiday会议中心给挤爆了，今年由于发行B级普通股的关系使得我们的股东人数又增加了整整一倍，因此我们决定把开会的场地移到可以容纳10,000人同时备有宽广停车场的阿肯萨本体育馆，大门会在当天早上七点开放，同时在八点半，我们会播放由财务长Marc Hamburg制作的全新伯克希尔电影短片供大家欣赏（伯克希尔所有人都必须身兼数职）。",
    
    "Overcoming our legendary repugnance for activities even faintly commercial":
        "为了克服大家对于商业气息的厌恶，我们在会场外大厅备有伯克希尔各式各样的产品供大家选购，去年我们打破记录，总共卖出1,270磅的糖果、1,143双的鞋子以及价值超过29,000美元的世界百科全书与相关出版品，外加700只由旗下子公司Quikut所生产的小刀，另外在现场许多股东询问有关盖可汽车保险的信息，如果你想在汽车保险费上省一笔钱，记得把你现在的保单带到现场，我们估计至少有40%的股东可以因此而节省不少保费（我很想说100%，不过保险业实务的经营并非如此，因为每家保险业者对于风险的估计都不同，事实上我们有些股东支付的保费就比跟盖可投保要来得低）。",
    
    "An attachment to the proxy material":
        "后面附有股东会开会投票的相关资料，跟各位解释如何拿到入场所许的识别证，由于预期会有相当多的人与会，我们建议大家最好先预订机位与住宿，美国运通（电话800-799-6634）将会很高兴为您提供相关安排服务，如同以往，我们会安排巴士接送大家往返各大旅馆与会场之间，并在会后接送大家到内布拉斯加家具店与波仙珠宝店或是到饭店与机场。",
    
    "NFM's main store":
        "占地75英亩的NFM主馆距离会场约1英哩远，营业时间平日从早上10点到下午9点，星期六从早上10点到下午6点，星期日则从中午开到下午6点，记得去向Rose Blumkin-B太太问好，她今年高龄103岁，有时还会戴上氧气罩在轮椅上工作，不过如果你想要跟上她的脚步，需要氧气的可能是你，NFM去年的营业额高达2.65亿美元，这是全美单一家具店营业的新高记录，记得去现场查一查商品的种类与标价，你就会知道原因了。",
    
    "Borsheim's normally is closed on Sunday":
        "平时礼拜天不营业的波仙珠宝，特地在五月四日股东会当天为股东与来宾开放，从中午开到下午6点，去年在星期六股东会前一天，我们打破了波仙单日的订单量与营业额记录，当然还包括每平方英吋的参观人数记录，今年我们考量到参观人数还会再增加，所以大家在当天一定要准备好入场证，当然不想人挤人的股东可以选择在前一天或后一天前往参观，星期六从早上10点开到下午5点半，星期一则从早上10点开到晚上8点，无论如何今年大家一定要来看看波仙的总裁Susan是如何施展她的技巧将你的荷包给掏空。",
    
    "My favorite steakhouse":
        "我个人最爱的牛排馆Gorat's去年在股东年会的那个周末完全客满，虽然临时还在星期天下午四点多排出的一个空档，今年该餐厅从四月一号开始接受预订（电话402-551-3733），我会在星期天参加完波仙珠宝的活动后到Gorat's享用我最常点的丁骨牛排加上双份的肉丸，当然我也推荐我的宝贝助理Debbie标准的菜单——生烤牛肉三明治外加马铃薯泥与肉汤，记得报上Debbie的名号，你就可以多得到一碗肉汤。",
    
    "The Omaha Royals":
        "在前一天5月3日，星期六晚上，Rosenblatt体育馆将会有一场奥玛哈皇家队对印第安纳波利斯印第安人队的比赛，一如往年轮到由我先发，每一年就投那么一球。",
    
    "Though Rosenblatt is normal in appearance":
        "虽然Rosenblatt球场的外观看起来与其它球场没有多大的不同，不过它的投手丘地形却相当特殊，有时会发出特殊的重力短波，导致本来很平稳投出的球突然急速往下坠，过去有好几次我都成为这种怪异自然现象的受害者，不过我还是希望今年的情况会好一点，虽然当天会场有许多拍照的机会，不过我还是奉劝大家的快门要抓准一点，才能完整捕捉由我投出向本垒板急速奔去的快速球。",
    
    "Our proxy statement includes information about obtaining tickets to the game":
        "股东会资料将告诉大家如何取得球赛入场的门票，同时我们也会提供星期天晚上会开张的餐厅信息，同时列出假日期间在奥玛哈你可以从事的活动介绍，伯克希尔总部所有成员都期待能够见到大家。",
    
    # 投资建议
    "Your goal as an investor should simply be to purchase":
        "作为投资者，你的目标应当仅仅是找到一个你能理解的、在未来5年、10年和20年内其收益肯定会大幅增长的公司部分股权。随着时间的推移，你会发现只有少数几家公司符合这些标准——所以当你发现一家符合条件的公司时，你应该买入相当数量的股票。你还必须抵制让你偏离指导方针的诱惑：如果你不愿意持有一只股票十年，那就不要连十分钟都持有。把这些总收益逐年上升的公司组合在一起，你投资组合的市值自然也会上升。",
    
    "Though it's seldom recognized, this is the exact approach that has produced gains for Berkshire shareholders":
        "虽然这很少被认识到，但这正是为伯克希尔的股东带来收益的精确方法：我们的透视盈余在过去几年间大幅跃进，而同期间我们的股票价格也跟着大涨。要不是我们的盈余大幅增加，伯克希尔所代表的价值就不可能大幅增长。",
    
    "The greatly enlarged earnings base we now enjoy":
        "我们现在拥有的庞大的收益基础，将不可避免地导致我们未来的收益增长落后于过去。但是，我们会继续朝着一贯的方向努力。我们将通过良好地经营现有业务来增加收益——这是一项因我们的运营经理人才华横溢而变得容易的工作——并通过收购其他不会因变革而动荡、且拥有重要竞争优势的业务来增加收益，无论是全部还是部分收购。",
    
    # 续表部分的翻译
    "In this table, we have calculated our float by adding loss reserves":
        "表中的浮存金计算方式为：将所有损失准备、损失费用调整准备、假设再保险持有的资金及未赚取保费相加，再扣除应付佣金、预付并购成本、预付税款及相关再保递延费用。相对于我们的保费收入总额，我们的浮存金部位算是相当大的，至于浮存金的成本则决定于所发生的承保损失或利益而定，在某些年度，就像是最近四年，由于我们有承保利益，所以换句话说，我们的资金成本甚至是负的，光是持有这些资金我们就已经开始赚钱了。",
    
    "Since 1967, when we entered the insurance business":
        "自从1967年我们进军保险业以来，我们的浮存金每年以22.3%复合率增加，大部分的年度，我们的资金成本都在零以下，受惠于这些免费的资金，伯克希尔的绩效大大的提升了。更甚者，在完成对GEICO的并购之后，我们取得免费资金的成长速度又加快了许多。",
    
    # GEICO续
    "GEICO's growth would mean nothing if it did not produce reasonable underwriting profits":
        "如果不能产生合理的承保利润，GEICO的增长就毫无意义。这里也有好消息：去年，我们不仅实现了承保目标，还超出了一些。不过，我们的目标不是扩大利润率，而是扩大我们为客户提供的价格优势。鉴于这一策略，我们相信1997年的增长将轻松超过去年。",
    
    # 通用翻译补充
    "Should you choose, however, to construct your own portfolio":
        "不过，如果你选择建立自己的投资组合，有一些想法值得记住。聪明的投资并不复杂，尽管这远非易事。投资者真正需要的是正确评估所选企业的能力。注意"所选"这个词：你不必成为每家公司的专家，甚至许多公司都不需要。你只需要能够评估你能力圈范围内的公司。能力圈的大小并不重要；然而，知道它的边界在哪里才是至关重要的。",
    
    "To invest successfully, you need not understand beta":
        "要成功地投资，你不需要了解贝塔系数、有效市场理论、现代投资组合理论、期权定价或新兴市场。事实上，你可能更好的是对这些一无所知。当然，这并不是大多数商学院的主流观点，这些学校的金融课程往往被这些学科所主导。然而，在我们看来，投资学生只需要两门教得好的课程——如何评估企业价值，以及如何思考市场价格。",
    
    # USAir续
    "Facing this penalty provision":
        "面对这样的惩罚条款将督促美国航空尽快清偿对我们的欠款，而等到1996年下半年美国航空开始转亏为盈时，他们果真开始清偿这笔合计4,790万美元的欠款，为此我们特别要感谢美国航空现任总裁Stephen Wolf，是他让这家落难的航空公司得以付出这笔钱，同时美国航空的表现也归因于航空业景气复苏，当然该公司还是有成本结构的问题有待解决。",
    
    "Early in 1996, before any accrued dividends had been paid":
        "在稍早1996年初，我们还尚未收到积欠的股息之前，我再度尝试以3.35亿美元把这笔投资卖掉，所幸这次的举动又没有成功，使得我们得以从胜利之神口中逃过失败的命运。",
    
    # 报告收益来源
    "The table that follows shows the main sources of Berkshire's reported earnings":
        "下表显示了伯克希尔报告收益的主要来源。在这个表述中，购买法会计调整不分配给所适用的特定业务，而是汇总单独列示。这种程序让你能够以如果我们没有收购这些企业，它们本来会被报告的方式来查看我们企业的收益。由于第65和66页讨论的原因，这种形式的表述在我们看来对投资者和管理者都更有用，而不是使用一般公认会计原则（GAAP），后者要求将收购溢价逐个业务冲销。当然，我们在表格中显示的总收益与审计财务报表中的GAAP总额相同。",
}

def count_chinese_chars(text):
    """统计中文字符数量"""
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    return len(chinese_pattern.findall(text))

def count_en_chars(text):
    """统计英文字符数量"""
    en_pattern = re.compile(r'[a-zA-Z]')
    return len(en_pattern.findall(text))

def strip_tags(text):
    """移除HTML标签"""
    return re.sub(r'<[^>]+>', '', text)

def extract_blocks(html_content):
    """提取所有双语块"""
    blocks = []
    block_pattern = re.compile(
        r'<div class="bilingual-block">(.*?)</div>\s*</div>\s*</div>\s*</div>',
        re.DOTALL
    )
    
    # 改用更简单的方法：找到所有的bilingual-block
    pattern = re.compile(
        r'<div class="bilingual-block">(.*?)</div>\s*</div>\s*</div>\s*</div>',
        re.DOTALL
    )
    
    # 简化方法：逐个提取lang-block
    for match in re.finditer(r'<div class="bilingual-block">', html_content):
        start = match.start()
        # 找到下一个bilingual-block或结束标记
        next_block = html_content.find('<div class="bilingual-block">', start + 1)
        if next_block == -1:
            next_block = html_content.find('</article>', start)
        if next_block == -1:
            next_block = len(html_content)
        
        block_content = html_content[start:next_block]
        blocks.append((start, next_block, block_content))
    
    return blocks

def parse_bilingual_block(block_content):
    """解析双语块，返回英文和中文内容"""
    # 提取英文部分
    en_match = re.search(
        r'<div class="lang-block lang-en">.*?<span class="lang-label">English</span>(.*?)</div>',
        block_content, re.DOTALL
    )
    en_text = en_match.group(1) if en_match else ""
    en_text = strip_tags(en_text).strip()
    
    # 提取中文部分
    cn_match = re.search(
        r'<div class="lang-block lang-cn">.*?<span class="lang-label">中文翻译</span>(.*?)</div>',
        block_content, re.DOTALL
    )
    cn_text = cn_match.group(1) if cn_match else ""
    cn_text = strip_tags(cn_text).strip()
    
    return en_text, cn_text

def find_best_translation(en_text, reference_translations):
    """根据英文内容找到最佳参考翻译"""
    for key, value in reference_translations.items():
        if key.lower() in en_text.lower() or en_text.lower() in key.lower():
            return value
    return None

def fix_html_file():
    """修复HTML文件中的不完整翻译"""
    global html_content
    
    blocks = extract_blocks(html_content)
    fixed_count = 0
    incomplete_blocks = []
    
    for start, end, block_content in blocks:
        en_text, cn_text = parse_bilingual_block(block_content)
        
        # 跳过空块
        if not en_text or not cn_text:
            continue
        
        # 跳过纯分隔符
        if set(en_text.replace('*', '').replace('-', '').replace(' ', '')) == set():
            continue
            
        en_len = count_en_chars(en_text)
        cn_len = count_chinese_chars(cn_text)
        
        # 计算比例
        if en_len > 0:
            ratio = cn_len / en_len
        
            # 如果中文不到英文的50%，则需要补全
            if ratio < 0.5 and en_len > 50:
                incomplete_blocks.append({
                    'en': en_text[:200] + '...' if len(en_text) > 200 else en_text,
                    'cn': cn_text,
                    'en_len': en_len,
                    'cn_len': cn_len,
                    'ratio': ratio,
                    'start': start,
                    'end': end
                })
    
    print(f"发现 {len(incomplete_blocks)} 个翻译不完整的双语块")
    
    # 打印一些示例
    print("\n前10个不完整块的示例：")
    for i, block in enumerate(incomplete_blocks[:10]):
        print(f"\n{i+1}. 英文长度: {block['en_len']}, 中文长度: {block['cn_len']}, 比例: {block['ratio']:.2%}")
        print(f"   英文: {block['en'][:100]}...")
        print(f"   中文: {block['cn'][:100]}...")
    
    return incomplete_blocks

if __name__ == "__main__":
    incomplete_blocks = fix_html_file()
    print(f"\n总计: {len(incomplete_blocks)} 个块需要补全翻译")
