
EXEC sp_configure 'cost threshold for parallelism', 5;
EXEC sp_configure 'max degree of parallelism', 0;
EXEC sp_configure 'optimize for ad hoc workloads', 0;
RECONFIGURE;