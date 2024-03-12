val joinCondition = (1 to 20).map(i => (org_table(s"level$i") === bbs_table("access_object")) || (org_table(s"level$i") === ("CA-" + bbs_table("access_object")))).reduce(_ || _)
