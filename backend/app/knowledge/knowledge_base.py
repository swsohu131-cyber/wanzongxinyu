"""
万宗心悟AI疗愈智能体 - 三位一体知识库
融合哲学、心理学、宗教学，构建正向疗愈知识体系
遵循白皮书六大核心原则：
- 非传教原则：剥离宗教形式，保留精神疗愈属性
- 三元融合原则：三者有机融合，不偏向任一学科
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import uuid


class KnowledgeDomain(Enum):
    PHILOSOPHY = "philosophy"
    PSYCHOLOGY = "psychology"
    RELIGION = "religion"


@dataclass
class KnowledgeEntry:
    id: str
    domain: KnowledgeDomain
    category: str
    title: str
    content: str
    keywords: List[str]
    target_issues: List[str]
    cultural_tags: List[str]
    source: str
    weight: float = 0.5


class TrinityKnowledgeBase:
    def __init__(self):
        self.entries: Dict[str, KnowledgeEntry] = {}
        self._initialize_knowledge_base()

    def _initialize_knowledge_base(self):
        self._load_philosophy_knowledge()
        self._load_psychology_knowledge()
        self._load_religion_knowledge()

    def _load_philosophy_knowledge(self):
        philosophy_entries = [
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PHILOSOPHY,
                category="存在主义",
                title="存在先于本质",
                content="人首先是存在的，然后才是自己选择的样子。不是你应该成为谁，而是你想成为谁。你的每一个选择都在定义你自己。这意味着你永远有选择的自由，哪怕面对困境，你也可以选择如何回应。",
                keywords=["存在", "选择", "自由", "自我", "本质"],
                target_issues=["存在焦虑", "价值虚无", "选择困难", "自我怀疑"],
                cultural_tags=["西方", "现代"],
                source="萨特"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PHILOSOPHY,
                category="存在主义",
                title="直面虚无创造意义",
                content="生活本身没有固定的意义，但正因为如此，你可以为自己的生活创造意义。意义不是找到的，而是活出来的。每一天的小事、每一次真诚的连接、每一个用心的选择，都是你在编织生命的意义。",
                keywords=["虚无", "意义", "创造", "生活", "选择"],
                target_issues=["空虚感", "无聊感", "找不到目标", "生活无意义"],
                cultural_tags=["西方", "现代"],
                source="萨特"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PHILOSOPHY,
                category="儒家思想",
                title="尽心即心安",
                content="做事情的时候，只要尽心尽力就好，不必太在意结果。过程做好了，结果自然会来。与其担忧未来，不如好好把握现在这一刻。",
                keywords=["尽心", "心安", "当下", "努力"],
                target_issues=["焦虑", "担忧未来", "患得患失", "过分在意结果"],
                cultural_tags=["中国", "儒家", "东亚"],
                source="孟子"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PHILOSOPHY,
                category="道家思想",
                title="顺其自然为所当为",
                content="很多事情不是我们能控制的，就像天气、像别人的想法。学会接受那些我们改变不了的，然后把自己能做的事情做好。这就是道家说的顺其自然——不是躺平，而是一种智慧地分配精力的方式。",
                keywords=["自然", "接受", "放下", "顺应"],
                target_issues=["执念", "控制欲", "焦虑", "完美主义"],
                cultural_tags=["中国", "道家", "东亚"],
                source="道德经"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PHILOSOPHY,
                category="生命哲学",
                title="生命是一个过程",
                content="很多人把生命当成一场考试或者任务清单，总觉得要达成某个目标人生才算圆满。但其实生命本身就是一个礼物，每一个当下都是独一无二的。别急着赶路，忘了看看路边的风景。",
                keywords=["过程", "当下", "体验", "生命"],
                target_issues=["目标焦虑", "急于求成", "忽略当下", "生命意义"],
                cultural_tags=["普遍"],
                source="综合"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PHILOSOPHY,
                category="处世哲学",
                title="做减法比做加法更重要",
                content="现代人总觉得拥有的越多越幸福，但有时候少一些反而更轻松。那些真正重要的东西，其实很少。把注意力从我还有什么没得到转到我拥有什么，你会发现其实你已经拥有了很多。",
                keywords=["放下", "知足", "简单", "幸福"],
                target_issues=["物欲", "攀比", "焦虑", "不满足"],
                cultural_tags=["普遍", "现代"],
                source="综合"
            ),
            # ========== 新增哲学思想 ==========
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PHILOSOPHY,
                category="斯多葛学派",
                title="控制能控制的，放下不能控制的",
                content="生活中很多痛苦来自于我们试图控制那些超出我们能力范围的事情——别人的想法、未来的结果、自然的法则。斯多葛哲学告诉我们：专注于我们能控制的东西（我们的选择、态度、努力），接受我们不能控制的（别人的看法、命运的安排）。这样内心才能获得平静。",
                keywords=["斯多葛", "控制", "接受", "平静", "放下"],
                target_issues=["焦虑", "控制欲", "完美主义", "患得患失"],
                cultural_tags=["西方", "古希腊", "古罗马"],
                source="爱比克泰德"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PHILOSOPHY,
                category="斯多葛学派",
                title="苦难是成长的机会",
                content="斯多葛学派认为，困难和挫折不是诅咒，而是锻炼性格的机会。就像肌肉需要阻力才能强壮，心灵也需要挑战才能成长。每一个困难都蕴含着学习的机会。",
                keywords=["苦难", "成长", "坚韧", "斯多葛"],
                target_issues=["逆境", "挫折", "困难", "抗压"],
                cultural_tags=["西方", "古希腊", "古罗马"],
                source="马可·奥勒留"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PHILOSOPHY,
                category="阳明心学",
                title="知行合一",
                content="知道和做到是两回事。真正的知道，是能够做到的；做不到的，其实不是真正的知道。王阳明说：知是行的开始，行是知的完成。比如你知道要放下，但做不到，说明还没有真正知道。试着在每一个当下把知道的道理活出来。",
                keywords=["知行合一", "王阳明", "心学", "实践", "行动"],
                target_issues=["知而不行", "拖延", "知道但做不到", "执行力"],
                cultural_tags=["中国", "儒家", "东亚"],
                source="王阳明"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PHILOSOPHY,
                category="阳明心学",
                title="致良知",
                content="每个人都有辨别是非的本能，这种内在的道德感就是'良知'。但日常生活中，我们的私欲和偏见会蒙蔽良知，让人做出违背内心的选择。修炼的方法是：静下来，问问自己的良知怎么说的，然后依此行动。",
                keywords=["良知", "王阳明", "心学", "道德", "内心"],
                target_issues=["选择困难", "道德困惑", "迷失自我", "内心矛盾"],
                cultural_tags=["中国", "儒家", "东亚"],
                source="王阳明"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PHILOSOPHY,
                category="尼采哲学",
                title="杀不死我的使我更强大",
                content="尼采的这句话告诉我们，生命的挫折和苦难可以成为力量的源泉。经历过大困难的人，往往拥有更强的韧性和更深的智慧。关键不在于避免痛苦，而在于如何面对和超越痛苦。",
                keywords=["尼采", "坚韧", "超越", "痛苦", "成长"],
                target_issues=["创伤", "挫折", "逆境", "心理创伤"],
                cultural_tags=["西方", "现代"],
                source="尼采"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PHILOSOPHY,
                category="尼采哲学",
                title="每一个不曾起舞的日子都是对生命的辜负",
                content="生命只有一次，而且它正在流逝。不要把生命花在等待完美的时刻，不要等到'以后'才开始好好生活。每一个今天都是礼物，都是你可以真正活着的日子。",
                keywords=["尼采", "活在当下", "生命", "珍惜", "行动"],
                target_issues=["拖延", "等待", "生活无意义", "虚度光阴"],
                cultural_tags=["西方", "现代"],
                source="尼采"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PHILOSOPHY,
                category="叔本华哲学",
                title="人生就是一场钟摆",
                content="叔本华说人生就像钟摆，在欲望和无聊之间摇摆。满足了一个欲望，马上又想要下一个，永远没有尽头。真正的解脱不是不断满足欲望，而是减少不必要的欲望，看到已经拥有的东西。这样内心才能平静。",
                keywords=["叔本华", "欲望", "知足", "内心平静", "放下"],
                target_issues=["物欲", "永不满足", "攀比", "空虚"],
                cultural_tags=["西方", "现代"],
                source="叔本华"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PHILOSOPHY,
                category="苏格拉底",
                title="认识你自己",
                content="古希腊德尔斐神庙上刻着这句话：认识你自己。这是一切智慧的开始。很多人一生都在向外追求——追求成功、财富、认可——却很少向内看，了解自己真正想要的是什么。定期给自己一些独处的时间，问问自己：我真正在乎的是什么？",
                keywords=["苏格拉底", "认识自己", "自我探索", "内省", "价值观"],
                target_issues=["迷茫", "不知道想要什么", "迷失", "自我认知"],
                cultural_tags=["西方", "古希腊"],
                source="苏格拉底"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PHILOSOPHY,
                category="庄子思想",
                title="无用之用方为大用",
                content="世人都追求'有用'——有用的技能、有用的关系、有用的资源。但庄子告诉我们，有时候看起来'无用'的东西，其实最有价值。比如发呆、休息、无目的地散步...这些'无用'的活动，恰恰是让心灵恢复活力的时刻。别把自己逼得太紧，无用之事是生活的调剂。",
                keywords=["庄子", "无用", "休息", "放松", "慢生活"],
                target_issues=["过度工作", "效率焦虑", "不会休息", "紧绷"],
                cultural_tags=["中国", "道家", "东亚"],
                source="庄子"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PHILOSOPHY,
                category="亚里士多德",
                title="中庸之道",
                content="亚里士多德说，美德处于两个极端之间。比如勇敢是懦弱和鲁莽之间，温和是冷漠和暴怒之间。不是要我们平庸，而是要找到最恰当的状态。这需要智慧和判断力，在不同情境中找到平衡点。",
                keywords=["亚里士多德", "中庸", "平衡", "美德", "智慧"],
                target_issues=["极端思维", "非黑即白", "情绪波动", "人际关系"],
                cultural_tags=["西方", "古希腊"],
                source="亚里士多德"
            ),
        ]
        for entry in philosophy_entries:
            self.entries[entry.id] = entry

    def _load_psychology_knowledge(self):
        psychology_entries = [
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PSYCHOLOGY,
                category="认知调整",
                title="想法不是事实",
                content="我们脑子里经常会出现一些很绝对的想法，比如我真没用或者事情永远不会变好。但这些只是想法，不是事实。试着问自己：这是真的吗？有什么证据？有没有其他可能？",
                keywords=["认知", "想法", "事实", "证据", "重新评估"],
                target_issues=["负面思维", "抑郁情绪", "焦虑思维", "自我否定"],
                cultural_tags=["西方", "现代"],
                source="认知行为疗法"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PSYCHOLOGY,
                category="认知调整",
                title="区分观察与评论",
                content="我们很容易把我做了这件事变成我就是这样的人。比如偶尔一次失误就说我总是这么笨。试着就事论事，今天的事就留在今天，别把它变成对整个人的评价。",
                keywords=["观察", "评论", "就事论事", "自我评价"],
                target_issues=["过度自责", "自我否定", "完美主义", "低自尊"],
                cultural_tags=["普遍"],
                source="非暴力沟通"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PSYCHOLOGY,
                category="正念",
                title="感受情绪而不是被情绪控制",
                content="情绪来了，不要急着赶走它，也不用认同它。只是承认我现在感到难过，然后看看这个情绪在身体里是什么感觉。给它空间，它反而会慢慢流走。正念不是要你开心，而是让你如实面对此刻。",
                keywords=["正念", "情绪", "觉察", "接纳"],
                target_issues=["情绪波动", "无法控制情绪", "焦虑", "压抑情绪"],
                cultural_tags=["普遍", "东方", "西方"],
                source="正念减压"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PSYCHOLOGY,
                category="自我接纳",
                title="先照顾好自己",
                content="很多人觉得满足自己的需求是自私的。但如果你把自己耗尽了，你也帮不了任何人。照顾好自己不是自私，而是你能持续付出的前提。飞机安全讲解说的好：先给自己戴好氧气面罩，再帮旁边的人。",
                keywords=["自我关怀", "自爱", "界限", "照顾自己"],
                target_issues=["讨好型人格", "界限不清", "自我忽视", "倦怠"],
                cultural_tags=["普遍"],
                source="心理学"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PSYCHOLOGY,
                category="人际交往",
                title="别人怎么看你 是别人的事",
                content="我们之所以在乎别人的看法，是因为人类天生需要归属感。但成熟意味着你可以承受被误解、被讨厌的压力。你无法控制别人怎么想，你能做的是活出自己的价值观。",
                keywords=["他人看法", "归属感", "价值观", "内在评价"],
                target_issues=["在意他人眼光", "社交焦虑", "取悦他人", "害怕被讨厌"],
                cultural_tags=["普遍"],
                source="心理学"
            ),
            # ========== 新增心理学疗法 ==========
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PSYCHOLOGY,
                category="DBT接纳承诺疗法",
                title="接纳是改变的开始",
                content="DBT（辩证行为疗法）告诉我们一个反直觉的道理：越是抗拒痛苦，痛苦越强烈。试着接纳当下的感受——不是认同痛苦，而是承认'我现在确实感到难过'。在接纳的基础上，再选择有价值的行动。这比强迫自己'不要难过'更有效。",
                keywords=["DBT", "接纳", "承诺行动", "情绪调节", "正念"],
                target_issues=["情绪调节", "边缘人格", "冲动行为", "情绪波动"],
                cultural_tags=["西方", "现代"],
                source="DBT疗法"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PSYCHOLOGY,
                category="DBT接纳承诺疗法",
                title="痛苦的普遍性",
                content="DBT核心理念之一：痛苦是人类共同的经历，每个人都在承受着某种形式的痛苦。不只是你。这不是要你轻视自己的痛苦，而是让你知道：你不是孤独的。这种'普遍性'的感知能减轻羞耻感。",
                keywords=["DBT", "痛苦", "普遍性", "联结", "共情"],
                target_issues=["孤独感", "羞耻感", "觉得我最惨", "孤立"],
                cultural_tags=["西方", "现代"],
                source="DBT疗法"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PSYCHOLOGY,
                category="EMDR眼动脱敏",
                title="创伤可以处理",
                content="EMDR（眼动脱敏与再加工）是一种专门处理创伤的心理疗法。它发现，当大脑处理创伤记忆时，如果同时给予双侧刺激（如眼动），可以帮助大脑重新整合这些记忆，让创伤不再是困扰你的'活生生的过去'。",
                keywords=["EMDR", "创伤", "眼动脱敏", "PTSD", "心理创伤"],
                target_issues=["心理创伤", "PTSD", "创伤后应激", "童年阴影"],
                cultural_tags=["西方", "现代"],
                source="EMDR疗法"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PSYCHOLOGY,
                category="正念认知疗法MBCT",
                title="想法不是事实",
                content="MBCT（正念认知疗法）发现：抑郁复发的人，常常被'反刍思维'困扰——一遍遍回想负面事件和想法。正念帮助我们与想法保持距离，认识到'我有一个想法'和'这个想法是真的'是两回事。",
                keywords=["MBCT", "正念", "反刍思维", "抑郁", "认知"],
                target_issues=["抑郁症", "反刍思维", "负面思维", "抑郁复发"],
                cultural_tags=["西方", "现代", "东方"],
                source="MBCT疗法"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PSYCHOLOGY,
                category="完形疗法",
                title="此时此地",
                content="完形（Gestalt）疗法强调'此时此地'的力量。很多痛苦来自于对过去的懊悔或对未来的担忧，而忽略了'现在'这个唯一真实存在的时刻。试着把注意力带回当下：你现在听到什么、感受到什么、看到什么？",
                keywords=["完形", "此时此地", "当下", "正念", "觉察"],
                target_issues=["焦虑未来", "懊悔过去", "无法专注", "活在头脑里"],
                cultural_tags=["西方"],
                source="完形疗法"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PSYCHOLOGY,
                category="完形疗法",
                title="整体大于部分之和",
                content="完形疗法认为，人不是孤立的部分（情绪、身体、思想的组合），而是一个完整的整体。当你感到'不对劲'但说不清哪里不对，这是你的整体在提醒你什么。学会倾听自己的整体感受，而不只是分析每个部分。",
                keywords=["完形", "整体", "觉察", "直觉", "内在智慧"],
                target_issues=["说不清的焦虑", "直觉", "身体感觉", "整合"],
                cultural_tags=["西方"],
                source="完形疗法"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PSYCHOLOGY,
                category="叙事疗法",
                title="你是自己故事的作者",
                content="叙事疗法认为，我们是通过'故事'来理解自己和生活。但我们往往只讲了问题故事，而忽略了其他可能性。试着重新审视你的故事：我的人生还有哪些被忽视的章节？那些面对困难的经历展示了什么样的我？",
                keywords=["叙事", "故事", "重新叙事", "自我认同", "赋能"],
                target_issues=["自我否定", "被问题定义", "缺乏自信", "受害者心态"],
                cultural_tags=["西方"],
                source="叙事疗法"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PSYCHOLOGY,
                category="情绪聚焦疗法EFT",
                title="情绪是信使",
                content="EFT（情绪聚焦疗法）告诉我们：情绪不是敌人，而是信使。每种情绪都在传递某种信息——愤怒告诉你需要保护边界，悲伤告诉你需要支持，恐惧告诉你需要注意危险。学会倾听情绪在说什么，而不是一味地压抑或逃避。",
                keywords=["EFT", "情绪", "情绪聚焦", "情绪智商", "情绪调节"],
                target_issues=["情绪隔离", "情绪调节困难", "不知道感受什么", "情绪表达"],
                cultural_tags=["西方"],
                source="EFT疗法"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PSYCHOLOGY,
                category="依恋理论",
                title="早期关系模式影响当下",
                content="依恋理论发现，我们童年与主要照顾者的关系，会形成内在的'工作模型'，影响我们成年后的亲密关系。了解自己的依恋风格——安全型、焦虑型、回避型还是混乱型——可以帮助你理解自己在关系中的反应模式，从而做出不同的选择。",
                keywords=["依恋", "亲密关系", "童年", "关系模式", "依恋风格"],
                target_issues=["亲密关系问题", "依赖", "回避", "信任问题", "童年创伤"],
                cultural_tags=["西方"],
                source="依恋理论"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.PSYCHOLOGY,
                category="家庭系统排列",
                title="每个人在自己的位置上",
                content="家庭系统排列发现，在一个家庭中，每个成员都需要被承认、被赋予属于他们的位置。当某个位置被忽视或僭越，系统就会失衡。这不是玄学，而是提醒我们：尊重每个家庭成员的序位，不越位、不替代，是家庭和谐的基础。",
                keywords=["家庭系统", "序位", "系统排列", "家庭治疗", "关系"],
                target_issues=["家庭矛盾", "代际问题", "越位", "归属感"],
                cultural_tags=["西方"],
                source="家庭系统排列"
            ),
        ]
        for entry in psychology_entries:
            self.entries[entry.id] = entry

    def _load_religion_knowledge(self):
        religion_entries = [
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="佛教智慧",
                title="放下执念获得平静",
                content="很多痛苦来自于想要抓住某些东西——想要事情按照我们想要的方式发展，想要某些人永远不离开。但一切都在变化，这就是生命的本质。学会接受无常，不是放弃，而是给自己松绑。",
                keywords=["放下", "执念", "无常", "接受", "平静"],
                target_issues=["执念", "失去恐惧", "控制欲", "痛苦"],
                cultural_tags=["佛教", "东亚", "南亚"],
                source="佛教"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="佛教智慧",
                title="此刻即圆满",
                content="很多人在等待某个以后——等我有空了、等孩子长大了、等退休了。但生命的意义不在某个未来，而在每一个当下。如果你不能好好过今天，明天大概率也一样。",
                keywords=["当下", "圆满", "此刻", "珍惜"],
                target_issues=["等待未来", "拖延", "生活无意义", "焦虑"],
                cultural_tags=["佛教", "普遍"],
                source="佛教"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="基督教精神",
                title="宽恕他人解脱自己",
                content="记恨一个人，就像自己喝毒药却希望别人痛苦。放下别人的过错，不是便宜了别人，而是把自己从痛苦中释放出来。宽恕不代表认同对方的行为，而是选择让自己不再被这件事控制。",
                keywords=["宽恕", "放下", "自由", "释怀"],
                target_issues=["怨恨", "记仇", "人际关系痛苦", "愤怒"],
                cultural_tags=["基督教", "西方"],
                source="基督教"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="基督教精神",
                title="你被爱着不需要证明自己",
                content="很多人拼命努力，是因为觉得自己必须配得上被爱。但实际上，你的价值不是靠成就堆出来的。知道自己被爱、被接纳，不需要任何条件，这种感觉本身就足以支撑你度过困难。",
                keywords=["无条件的爱", "接纳", "自我价值", "安全感"],
                target_issues=["不配得感", "拼命证明自己", "低自尊", "缺爱"],
                cultural_tags=["基督教", "西方"],
                source="基督教"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="精神寄托",
                title="与更大的存在连接",
                content="有时候感到孤独和空虚，是因为我们只把自己当成一个孤立的个体。找到一个让自己感受到连接的方式——可以是冥想，自然、艺术、或者某种信仰。这种连接感会让你觉得自己的存在是有意义的。",
                keywords=["连接", "归属", "精神", "意义感"],
                target_issues=["孤独感", "空虚", "无意义感", "疏离"],
                cultural_tags=["普遍"],
                source="普遍精神"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="精神寄托",
                title="感恩能改变视角",
                content="当我们只盯着自己缺什么的时候，会觉得永远不够。但试着每天想想自己拥有的——哪怕是今天天气不错这样的小事。感恩不是自我欺骗，而是一种训练大脑看到更多的练习。",
                keywords=["感恩", "积极", "视角", "拥有"],
                target_issues=["不满足", "负面思维", "抱怨", "抑郁"],
                cultural_tags=["普遍"],
                source="积极心理学"
            ),
            # ========== 新增宗教智慧 ==========
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="伊斯兰教精神",
                title="托靠主，尽人事",
                content="伊斯兰教教导：做好自己该做的事（尽人事），然后把结果交给真主（托靠）。这意味着：努力但不执着结果，接受无法控制的事物。这不是宿命论，而是提醒我们专注于自己能做的，然后坦然面对结果。",
                keywords=["伊斯兰", "托靠", "尽人事", "接受", "放下执着"],
                target_issues=["焦虑结果", "患得患失", "控制欲", "执着"],
                cultural_tags=["伊斯兰", "中东", "穆斯林"],
                source="伊斯兰教"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="伊斯兰教精神",
                title="困难中有教训也有出路",
                content="《古兰经》中说：'真主不会给人超越其能力的考验。'这意味着，你遇到的困难是你可以承受的，而且每一个困难中既包含教训也包含出路。不要被困难吓倒，你比自己想象的更有韧性。",
                keywords=["伊斯兰", "考验", "韧性", "出路", "希望"],
                target_issues=["困难", "绝望", "觉得自己承受不了", "失去希望"],
                cultural_tags=["伊斯兰", "中东", "穆斯林"],
                source="古兰经"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="伊斯兰教精神",
                title="五件事在不知不觉中来临",
                content="圣训说：五件事在不知不觉中来临——死亡、幸福、灾难、战争、窃贼。因此，活着的每一天都是宝贵的。不要等到'以后'才去珍惜、才去和解、才去表达爱。现在就是最好的时刻。",
                keywords=["伊斯兰", "死亡", "活在当下", "珍惜", "无常"],
                target_issues=["拖延", "不珍惜当下", "后悔", "虚度"],
                cultural_tags=["伊斯兰", "中东", "穆斯林"],
                source="圣训"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="犹太教智慧",
                title="苦难是化了妆的祝福",
                content="犹太教卡巴拉传统认为，苦难不是惩罚，而是灵魂成长的机会。有时候，最困难的时刻恰恰是最大突破的前奏。不要急于评判一个困难的意义，时间会揭示它在你生命中的真正价值。",
                keywords=["犹太教", "苦难", "祝福", "成长", "卡巴拉"],
                target_issues=["苦难", "觉得被惩罚", "看不到意义", "绝望"],
                cultural_tags=["犹太教", "西方"],
                source="卡巴拉"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="犹太教智慧",
                title="选择比命运更重要",
                content="犹太教伦理强调：人始终有选择的自由。即使在最困难的环境中，你的选择依然定义着你这个人。重要的不是你遭受了什么，而是你如何回应。每一个选择都在塑造你的品格。",
                keywords=["犹太教", "选择", "自由意志", "回应", "品格"],
                target_issues=["无力感", "觉得没有选择", "受害者心态", "放弃"],
                cultural_tags=["犹太教", "西方"],
                source="犹太教伦理"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="印度教哲学",
                title="业力法则：种什么因得什么果",
                content="印度教的业力法则告诉我们：每一个行动、每一句话、每一个想法都会产生相应的后果。现在的处境是过去行为的结果，未来的处境取决于现在的选择。这意味着：你手中握有改变命运的力量。",
                keywords=["印度教", "业力", "因果", "选择", "责任"],
                target_issues=["抱怨命运", "不负责任", "等待改变", "无力"],
                cultural_tags=["印度教", "南亚", "东方"],
                source="印度教"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="印度教哲学",
                title="无常是生命的本质",
                content="印度教哲学认为，一切都在变化中——没有永恒不变的实体。这种'无常'不是悲观，而是提醒：好运会来也会走，困难也会来也会走。正因为一切都在流动，黑暗不会永远持续，光明也不会永远持续。",
                keywords=["印度教", "无常", "变化", "流动", "接纳"],
                target_issues=["执着", "害怕变化", "无法放下", "永恒思维"],
                cultural_tags=["印度教", "南亚", "东方"],
                source="印度教"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="印度教哲学",
                title="你就是答案",
                content="印度古籍《奥义书》说：'你就是你所寻找的。'很多人向外寻找意义、平静、答案——但真正的答案一直都在你内心。向内看，不是逃避世界，而是找到内心深处稳定的力量源泉。",
                keywords=["印度教", "内心", "自我", "智慧", "向内看"],
                target_issues=["向外寻找", "迷失", "不知道自己要什么", "内心空虚"],
                cultural_tags=["印度教", "南亚", "东方"],
                source="奥义书"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="耆那教",
                title="非暴力是最高的法则",
                content="耆那教教导'非暴力'（Ahimsa）为最高法则：不伤害任何生命。这不仅是外在行为，也包括内在的善意——不怀恨、不恶意揣测他人。即使无法完全做到，这个理念也能提醒我们：善意是生命的本质。",
                keywords=["耆那教", "非暴力", "善意", "不伤害", "慈悲"],
                target_issues=["愤怒", "怨恨", "恶意", "人际冲突"],
                cultural_tags=["印度教", "耆那教", "南亚"],
                source="耆那教"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="锡克教",
                title="神在每个人心中",
                content="锡克教的核心教导：神不在遥远的天上，而在你内心深处，也在每个人心中。这意味着：每个人都有神圣的本质，每个人都值得尊重。不必向外寻找神性，它就在你之内，在每一个人的生命之中。",
                keywords=["锡克教", "神性", "内在", "人人平等", "灵性"],
                target_issues=["觉得自己不够好", "评判他人", "灵性空虚", "向外寻找"],
                cultural_tags=["锡克教", "南亚"],
                source="锡克教"
            ),
            KnowledgeEntry(
                id=str(uuid.uuid4()),
                domain=KnowledgeDomain.RELIGION,
                category="巴哈伊信仰",
                title="合一是人类的命运",
                content="巴哈伊信仰认为，人类本来是一体，分离是幻象。虽然我们现在看到分歧和冲突，但人类走向合一是大势所趋。每一个促进理解、减少偏见的行为，都是在为这个合一的世界贡献力量。",
                keywords=["巴哈伊", "合一", "人类一体", "团结", "共同命运"],
                target_issues=["孤独感", "与他人疏离", "觉得孤立无援", "归属感"],
                cultural_tags=["巴哈伊", "普遍"],
                source="巴哈伊信仰"
            ),
        ]
        for entry in religion_entries:
            self.entries[entry.id] = entry

    def search(
        self,
        query: str,
        domain: Optional[KnowledgeDomain] = None,
        target_issue: Optional[str] = None,
        cultural_tags: Optional[List[str]] = None,
        limit: int = 5
    ) -> List[KnowledgeEntry]:
        results = []
        query_lower = query.lower()

        for entry in self.entries.values():
            if domain and entry.domain != domain:
                continue
            if target_issue and target_issue not in entry.target_issues:
                continue
            if cultural_tags:
                if not any(tag in entry.cultural_tags for tag in cultural_tags):
                    continue

            score = 0
            if query_lower in entry.title.lower():
                score += 3
            if query_lower in entry.content.lower():
                score += 2
            for kw in entry.keywords:
                if query_lower in kw.lower():
                    score += 1
            for issue in entry.target_issues:
                if query_lower in issue.lower():
                    score += 2

            if score > 0:
                entry.weight = score
                results.append(entry)

        results.sort(key=lambda x: x.weight, reverse=True)
        return results[:limit]

    def get_balanced_response(
        self,
        query: str,
        user_profile: Dict[str, Any]
    ) -> str:
        weights = user_profile.get("knowledge_weights", {
            "philosophy": 0.33,
            "psychology": 0.34,
            "religion": 0.33
        })

        total = 5
        philosophy_count = max(1, int(total * weights.get("philosophy", 0.33)))
        psychology_count = max(1, int(total * weights.get("psychology", 0.34)))
        religion_count = total - philosophy_count - psychology_count

        philosophy_results = self.search(query, domain=KnowledgeDomain.PHILOSOPHY, limit=philosophy_count)
        psychology_results = self.search(query, domain=KnowledgeDomain.PSYCHOLOGY, limit=psychology_count)
        religion_results = self.search(query, domain=KnowledgeDomain.RELIGION, limit=religion_count)

        all_results = philosophy_results + psychology_results + religion_results

        if cultural_tags := user_profile.get("cultural_background", {}).get("language"):
            all_results = [
                r for r in all_results
                if cultural_tags in r.cultural_tags or "普遍" in r.cultural_tags
            ]

        return all_results

    def get_knowledge_for_llm_context(
        self, 
        query: str, 
        user_profile: Dict[str, Any],
        limit: int = 5
    ) -> str:
        """
        生成供LLM使用的知识上下文字符串
        
        Args:
            query: 用户输入/问题
            user_profile: 用户画像，包含knowledge_weights和cultural_background
            limit: 返回的条目数量上限
        
        Returns:
            格式化的知识上下文字符串
        """
        weights = user_profile.get("knowledge_weights", {
            "philosophy": 0.33,
            "psychology": 0.34,
            "religion": 0.33
        })
        
        # 计算各领域应返回的条目数
        total = limit
        philosophy_count = max(1, int(total * weights.get("philosophy", 0.33)))
        psychology_count = max(1, int(total * weights.get("psychology", 0.34)))
        religion_count = total - philosophy_count - psychology_count
        
        # 搜索各领域相关知识
        philosophy_results = self.search(
            query, 
            domain=KnowledgeDomain.PHILOSOPHY, 
            limit=philosophy_count
        )
        psychology_results = self.search(
            query, 
            domain=KnowledgeDomain.PSYCHOLOGY, 
            limit=psychology_count
        )
        religion_results = self.search(
            query, 
            domain=KnowledgeDomain.RELIGION, 
            limit=religion_count
        )
        
        # 合并结果
        all_results = philosophy_results + psychology_results + religion_results
        
        # 如果没有匹配结果，使用通用知识
        if not all_results:
            all_results = list(self.entries.values())[:limit]
        
        # 格式化输出
        context_parts = []
        for entry in all_results:
            domain_name = {
                KnowledgeDomain.PHILOSOPHY: "【哲学】",
                KnowledgeDomain.PSYCHOLOGY: "【心理学】",
                KnowledgeDomain.RELIGION: "【宗教智慧】"
            }.get(entry.domain, "【其他】")
            
            context_parts.append(
                f"{domain_name}{entry.title}\n"
                f"{entry.content}\n"
                f"来源: {entry.source}"
            )
        
        return "\n\n".join(context_parts)

    def add_entry(self, entry: KnowledgeEntry):
        self.entries[entry.id] = entry

    def update_entry(self, entry_id: str, updates: Dict[str, Any]):
        if entry_id in self.entries:
            entry = self.entries[entry_id]
            for key, value in updates.items():
                if hasattr(entry, key):
                    setattr(entry, key, value)


knowledge_base = TrinityKnowledgeBase()
