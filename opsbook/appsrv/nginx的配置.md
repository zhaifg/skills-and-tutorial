# nginx
---

## secure_link_module 验证

secure_link $arg_md5, arg_expires;
secure_link_md5 "$secure_link_expires$uri imooc"

## geoip_module 模块
基于IP地址匹配 MaxMind GeoIP 二进制文件
geoip_country
geoip_city

if ($geoip_country_code != CN){
    
}

## https
