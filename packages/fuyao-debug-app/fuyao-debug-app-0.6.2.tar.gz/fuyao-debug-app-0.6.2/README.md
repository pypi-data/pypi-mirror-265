# Fuyao Debug App

通过命令行执行debug需求的功能，目前支持：  

0. 包含以下1-6所有功能的组合方法
1. 检查设备是否出现异常:
   - 1.1 从health checker中获取设备是否有硬件异常
   - 1.2 TODO - 从syslog中分析是否存在硬件告警及报错
2. 检查所有job相关node的log，是否有exception，分析exception
3. 检查是否有worker process退出
   - 3.1 检测日志中有没有worker退出的信息
   - 3.2 TODO - 检测主进程相关的子进程有没有退出, 比较数量？
4. 检查所有worker是否完成初始化
5. 自动收集各节点火焰图
6. 自动收集各节点rank的stack

