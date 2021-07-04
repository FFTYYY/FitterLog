DB_NAME = "fitterlog"
TB_NAME_NOUN_PRED_POS = "fitterlog_noun_predicate" # 名词id和谓词id到储存位置的映射
KEY_NOUN_CNT = (-1,-1) # 在fitterlog_noun_predicate中存名词id的位置
TB_NAME_PRED_ID = "fitterlog_predicate" # 谓词名到id的映射
KEY_PRED_CNT = "_fitterlog_count" # 在tb_name_predicate_id中存谓词id的位置


FILE_NAME_VALUE = "fitterlog-value"

CLAUSE_ROOT_NAME = "_fitterlog_root"
TB_NAME_CLAUSE = "fitterlog_clause"
CLAUSE_CONCAT = "-fitterlog-concat-" # 在clause的真实名中连接父名和子名的字符串

SENT_LOCK_PATH = "fitterlog/sentence/"
SENT_KEY_AMBI  = "fitterlog-ambiguity" # 直接名索引有歧义时的值

SENT_ATTR_DEFAULT = "default" # 表示default值的attr