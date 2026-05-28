from typing import Dict, List, Optional, Tuple
from models import Intent, DialogueState, Slot
import re
from datetime import datetime

class IntentRecognizer:
    INTENT_PATTERNS = {
        Intent.GREETING: [
            r"你好", r"您好", r"早上好", r"下午好", r"晚上好",
            r"hi", r"hello", r"嗨", r"在吗", r"在不在"
        ],
        Intent.STOCK_QUERY: [
            r"股票", r"股价", r"涨跌", r"上证", r"深证",
            r"A股", r"B股", r"蓝筹", r"大盘"
        ],
        Intent.FUND_QUERY: [
            r"基金", r"净值", r"收益率", r"定投", r"申购",
            r"赎回", r"分红", r"基金经理"
        ],
        Intent.INSURANCE_QUERY: [
            r"保险", r"投保", r"理赔", r"寿险", r"财险",
            r"医疗险", r"重疾险", r"车险"
        ],
        Intent.INVESTMENT_ADVICE: [
            r"投资", r"理财", r"配置", r"分散", r"风险",
            r"收益", r"建议", r"推荐"
        ],
        Intent.RISK_ASSESSMENT: [
            r"风险", r"评估", r"测评", r"承受能力", r"亏损",
            r"保守", r"激进", r"稳健"
        ],
        Intent.ACCOUNT_INFO: [
            r"账户", r"余额", r"密码", r"登录", r"实名",
            r"认证", r"绑定", r"银行卡"
        ],
        Intent.COMPLAINT: [
            r"投诉", r"不满", r"问题", r"错误", r"失败",
            r"不行", r"没用", r"糟糕"
        ],
        Intent.GOODBYE: [
            r"再见", r"拜拜", r"走了", r"退出", r"关闭",
            r"结束", r"感谢", r"谢谢"
        ]
    }
    
    def __init__(self):
        self.confidence_threshold = 0.3
    
    def recognize(self, text: str) -> Tuple[Intent, float]:
        text_lower = text.lower()
        scores = {}
        
        for intent, patterns in self.INTENT_PATTERNS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    score += 1
            if score > 0:
                scores[intent] = score / len(patterns)
        
        if not scores:
            return Intent.UNKNOWN, 0.0
        
        best_intent = max(scores, key=scores.get)
        confidence = scores[best_intent]
        
        return best_intent, confidence

class SlotFiller:
    SLOT_DEFINITIONS = {
        Intent.STOCK_QUERY: [
            Slot(name="stock_code", required=False, description="股票代码或名称"),
            Slot(name="time_range", required=False, description="时间范围"),
        ],
        Intent.FUND_QUERY: [
            Slot(name="fund_name", required=False, description="基金名称或代码"),
            Slot(name="fund_type", required=False, description="基金类型"),
        ],
        Intent.RISK_ASSESSMENT: [
            Slot(name="risk_level", required=False, description="风险等级"),
            Slot(name="investment_amount", required=False, description="投资金额"),
        ],
    }
    
    def extract_slots(self, text: str, intent: Intent) -> Dict[str, Slot]:
        slots = {}
        
        if intent in self.SLOT_DEFINITIONS:
            for slot_def in self.SLOT_DEFINITIONS[intent]:
                slots[slot_def.name] = Slot(
                    name=slot_def.name,
                    required=slot_def.required,
                    description=slot_def.description
                )
        
        stock_codes = re.findall(r'\d{6}', text)
        if stock_codes:
            slots['stock_code'] = Slot(name='stock_code', value=stock_codes[0], filled=True)
        
        money_patterns = re.findall(r'(\d+)\s*(万|亿|千)?\s*元', text)
        if money_patterns:
            slots['investment_amount'] = Slot(
                name='investment_amount',
                value=money_patterns[0][0],
                filled=True
            )
        
        time_patterns = re.findall(r'(今天|昨天|本周|上周|本月|近\d+天)', text)
        if time_patterns:
            slots['time_range'] = Slot(name='time_range', value=time_patterns[0], filled=True)
        
        return slots

class ResponseGenerator:
    INTENT_RESPONSES = {
        Intent.GREETING: [
            "您好！我是您的金融助手，很高兴为您服务。请问有什么金融问题我可以帮您解答？",
            "您好！请告诉我您想了解的金融信息，比如股票、基金、保险等方面。",
        ],
        Intent.STOCK_QUERY: [
            "关于股票投资，我建议您关注以下几点：\n1. 不要追涨杀跌\n2. 分散投资降低风险\n3. 关注基本面分析\n4. 长期持有优质股票",
        ],
        Intent.FUND_QUERY: [
            "基金投资适合长期规划。常见的基金类型包括：\n1. 股票型基金：高风险高收益\n2. 债券型基金：稳健收益\n3. 混合型基金：平衡风险\n4. 指数型基金：被动投资",
        ],
        Intent.INSURANCE_QUERY: [
            "选择保险时需要考虑：\n1. 保障范围是否全面\n2. 理赔条款是否宽松\n3. 保费是否合理\n4. 保险公司的实力和信誉",
        ],
        Intent.INVESTMENT_ADVICE: [
            "投资理财建议：\n1. 做好资产配置，不要把所有钱投入单一品种\n2. 根据自己的风险承受能力选择产品\n3. 长期投资比短期炒作更可靠\n4. 定期检视和调整投资组合",
        ],
        Intent.RISK_ASSESSMENT: [
            "风险评估是投资前的重要步骤。建议您：\n1. 评估自己的风险承受能力\n2. 不要投资超过自己承受能力的资金\n3. 了解产品的风险等级\n4. 做好止损预案",
        ],
        Intent.ACCOUNT_INFO: [
            "账户安全建议：\n1. 设置强密码并定期更换\n2. 开启双因素认证\n3. 不要在公共网络登录\n4. 警惕钓鱼网站和诈骗电话",
        ],
        Intent.COMPLAINT: [
            "非常抱歉给您带来不好的体验。请详细描述您遇到的问题，我会认真记录并反馈给相关团队处理。",
        ],
        Intent.GOODBYE: [
            "感谢您的咨询，祝您投资顺利！再见！",
            "很高兴为您服务，祝您生活愉快！再见！",
        ],
        Intent.UNKNOWN: [
            None,
        ],
    }
    
    def generate(self, intent: Intent, context: Optional[Dict] = None) -> Optional[str]:
        responses = self.INTENT_RESPONSES.get(intent, self.INTENT_RESPONSES[Intent.UNKNOWN])
        
        if responses[0] is None:
            return None
        
        if isinstance(context, dict) and 'slots' in context:
            slots = context['slots']
            response = responses[0]
            
            if slots.get('stock_code') and slots['stock_code'].get('value'):
                response += f"\n\n您查询的股票代码是：{slots['stock_code']['value']}"
            
            return response
        
        return responses[0]

class NLPEngine:
    def __init__(self):
        self.intent_recognizer = IntentRecognizer()
        self.slot_filler = SlotFiller()
        self.response_generator = ResponseGenerator()
        self.use_rag_fallback = True
    
    def process(self, text: str, current_intent: Optional[Intent] = None) -> Dict:
        intent, confidence = self.intent_recognizer.recognize(text)
        
        if confidence < 0.1 and current_intent:
            intent = current_intent
        
        slots = self.slot_filler.extract_slots(text, intent)
        
        response = self.response_generator.generate(intent, {'slots': slots})
        
        use_rag = False
        if response is None or intent == Intent.UNKNOWN or confidence < 0.3:
            use_rag = True
        
        return {
            'intent': intent,
            'confidence': confidence,
            'slots': {k: {'value': v.value, 'filled': v.filled, 'required': v.required}
                     for k, v in slots.items()},
            'response': response,
            'use_rag': use_rag
        }

nlp_engine = NLPEngine()
