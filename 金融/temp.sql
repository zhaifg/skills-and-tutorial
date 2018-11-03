THIRD_ACCOUNT

select count(1)  from ym_customer c  where  c.create_time <now()   and c.type=5 and c.create_time>='2018-04-17 00:00:00';

select c.pid  from ym_customer c  where  c.create_time <now()
and c.type=5 and c.create_time>='2018-04-17 00:00:00' order by c.create_time desc limit 0 , 20;


SELECT c.type,c.pid,c.account,c.mobile, c.origin,c.status, r.sfz_id,r.sex,r.target_area as area,
r.id_status,c.create_time, s.total_scope,s.total_consume,r.live_province,r.live_city,r.live_district,
jbs.nick_name,mb.mobileArea as mobile_area,c.micun_status,rr.bind_status is_recommended,
c.presalary_flag,prefanxian_flag,c.kf_id,sa.username kf_name,group_concat(cts.tag_name) tag_names
from ym_customer c LEFT JOIN ym_customer_resume r on c.pid=r.user_id  LEFT JOIN ym_customer_scope s
on s.user_id=c.pid   LEFT JOIN ym_customer_social  jbs on c.pid=jbs.user_id
left join ym_mobile_belong mb ON LEFT(c.mobile,7) = mb.mobileNumber
left join ym_recommend_relations rr ON c.pid=rr.recommended_id and rr.bind_status=1
 left join ym_callcenter_customer cc ON c.mobile=cc.call_number
 left join ym_customer_tags ct ON cc.pid=ct.user_id
 left join ym_customer_tag cts ON ct.tag_id=cts.pid
 left join ym_system_account sa ON c.kf_id=sa.pid  where 1=1   and
 c.pid in (4931579,4931574,4931572,4931567,4931566,4931549,4931547,
    4931545,4931544,4931538,4931537,4931532,4931531,4931522,4931520,4931519,
    4931517,4931513,4931511,4931506) group by c.pid order by c.create_time desc



SELECT c.pid,
c.account,
c.mobile,
c.create_time,
jbs.nick_name
from ym_customer c  LEFT JOIN ym_customer_social  jbs on c.pid=jbs.user_id
 where
  c.create_time <now()   and c.type=5 and c.create_time>='2018-04-17 00:00:00'
 group by c.pid order by c.create_time desc;


select *   from ym_customer_apply where user_id in (
 select c.pid  from ym_customer c  where  c.create_time <now()
and c.type=5 and c.create_time>='2018-04-17 00:00:00' order by c.create_time desc );
select ca.user_id, cy.qiye_name, cj.job_name, ca.audition_status, ca.audition_result from ym_customer_apply ca left join
         ym_company_job as cj on ca.job_id = cj.pid left join ym_company cy on
          cj.qiye_id=cy.pid where ca.user_id in (
             select c.pid  from ym_customer c  where  c.create_time <now()
            and c.type=5 and c.create_time>='2018-04-17 00:00:00' order by c.create_time desc
            );

select *   from ym_customer_apply where user_id in (
 select c.pid  from ym_customer c  where  c.create_time <now()
and c.type=5 and c.create_time>='2018-04-17 00:00:00' order by c.create_time desc );


,chenxia, zhangsy
,lujj,licb,zoudc


分享一个项目：
币圈传奇大空翼继iota的下一个物联网项目Linfinity
Linfinity致力于供应链场景的区块链技术应用，已和多家上市企业深度合作
现Linfinity空投活动正在进行中，进入社群奖励即价值10美金的邀请好友最高可以获得价值2000美元ToKen
链接：https://candy.linfinity.io/profile/90d5d5a82d1e4474eae57c395f9d3cb0
错过了iota,小蚁,本体 之后，2018年不能再错过Linfinity了

3+3 + 2 + 2

/ed89fcff44b966dfdefcceed5ae03a83

/c14c53cd368f1ca1e65ca68f1f61e400


cpu i7 8700
主板
内存: 16G
散热器
ssd 240
机箱 航嘉
电源500W 左右的


0.018018 bt 0.027369 0.048605

0.049928 -522.87 -69.63



1740.75

rcn 42.306579
