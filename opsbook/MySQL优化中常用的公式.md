#mysql优化中常用的公式
---

## Per-Thread Buffer memory utilization
(read_buffer_size + read_rnd_buffer_size + sort_buffer_size + thread_stack + join_buffer_size + binlog_cache_size) * max_connections

## Global Buffer memory utilization
innodb_buffer_pool_size + innodb_additional_mem_pool_size + innodb_log_buffer_size + key_buffer_size + query_cache_size

## Threads and Connections
thread_cache miss rate = Threads_created / Connections
connection ratio = (max_used_connections*100)/ max_connections
threads_per_second = threads_created / uptime

## Key Buffer
key_buffer_free = (key_blocks_unused * key_cache_block_size) / (key_buffer_size * 100)
key_cache_miss_rate = key_read_requests / key_reads

## Query Cache
query_cache_used_memory = query_cache_size – Qcache_free_memory
query_cache_mem_fill_ratio = ((query_cache_size – Qcache_free_memory) * 100) / query_cache_size
query_cache_percent_fragmented = (Qcache_free_blocks * 100) / Qcache_total_blocks

## Sorting
total_sorts = sort_scan + sort_range
passes_per_sort = sort_merge_passes / total_sorts

## Open Files
open_files_ratio = (open_files*100) / open_files_limit
if open_files_ratio > 80: increase open_files_limit

## Table Cache
table_cache_hit_rate = (open_tables*100) / opened_tables
table_cache_fill = (open_tables*100) / table_cache
if table_cache_fill < 95 && > 90: all good
if table_cache_fill < 90: decrease table_cache

## Table Locks
table_lock_miss_rate = table_locks_immediate / table_locks_waited
if table_lock_miss_rate > 4096: set concurrent_insert=2 and low_priority_updates=1

## Table Scans
full_table_scans= Handler_read_rnd_next / Com_select
if full_table_scans > 4096: increase read_buffer and read_rnd_buffer

## Join Buffer
if Select_full_join > 0: increase join_buffer
if Select_range_check > 0: increase join buffer
if Select_full_join = 0: join_buffer fine
if Select_range_check = 0: join buffer fine

## Temp tables
tmp_disk_tables= (created_tmp_disk_tables * 100)/( Created_tmp_tables + Created_tmp_disk_tables )
if tmp_disk_tables > 32: increase tmp_table_size

## InnoDB
innodb_buffer_pool_free_perc = (innodb_buffer_pool_pages_free*100) / innodb_buffer_pool_pages_total
innodb_index_size = SELECT SUM(INDEX_LENGTH) from information_schema.TABLES where ENGINE=’innodb’
innodb_data_size = SELECT SUM(DATA_LENGTH from information_schema.TABLES where ENGINE=’innodb’
