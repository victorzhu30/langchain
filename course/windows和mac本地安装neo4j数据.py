# 1.软件下载
# 1.下载Neo4j
# 下载地址：https://neo4j.com/deployment-center/
# 2.安装Java JDK
# 版本说明：https://neo4j.com/docs/operations-manual/current/installation/requirements/
# Java JDK下载：
# https://www.oracle.com/java/technologies/downloads/

# 2.软件安装
# 1.安装Java JDK
# java --version
# 2.安装neo4j
# Default login is username 'neo4j' and password 'neo4j' (full installation instructions below)
# # https://neo4j.com/download-thanks/?edition=community&release=2025.05.0&flavour=winzip#install

# D:\neo4j-community-2025.05.0\bin -> 右键 -> 在终端中打开 ->
# PS D:\neo4j-community-2025.05.0\bin> neo4j.bat console
# neo4j.bat : 无法将“neo4j.bat”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确
# 保路径正确，然后再试一次。
# 所在位置 行:1 字符: 1
# + neo4j.bat console
# + ~~~~~~~~~
#     + CategoryInfo          : ObjectNotFound: (neo4j.bat:String) [], CommandNotFoundException
#     + FullyQualifiedErrorId : CommandNotFoundException


# Suggestion [3,General]: 找不到命令 neo4j.bat，但它确实存在于当前位置。默认情况下，Windows PowerShell 不会从当前位置加载命令。如果信任此命令，请改为键入“.\neo4j.bat”。有关详细信息，请参阅 "get-help about_Command_Precedence"。
# PS D:\neo4j-community-2025.05.0\bin> .\neo4j.bat console
# WARNING: A terminally deprecated method in sun.misc.Unsafe has been called
# WARNING: sun.misc.Unsafe::objectFieldOffset has been called by org.jctools.util.UnsafeAccess (file:/D:/neo4j-community-2025.05.0/lib/jctools-core-4.0.5.jar)
# WARNING: Please consider reporting this to the maintainers of class org.jctools.util.UnsafeAccess
# WARNING: sun.misc.Unsafe::objectFieldOffset will be removed in a future release
# Directories in use:
# home:         D:\neo4j-community-2025.05.0
# config:       D:\neo4j-community-2025.05.0\conf
# logs:         D:\neo4j-community-2025.05.0\logs
# plugins:      D:\neo4j-community-2025.05.0\plugins
# import:       D:\neo4j-community-2025.05.0\import
# data:         D:\neo4j-community-2025.05.0\data
# certificates: D:\neo4j-community-2025.05.0\certificates
# licenses:     D:\neo4j-community-2025.05.0\licenses
# run:          D:\neo4j-community-2025.05.0\run
# Starting Neo4j.
# WARNING! You are using an unsupported Java runtime.
# * Please use Java(TM) 21 to run Neo4j.
# * Please see https://neo4j.com/docs/ for Neo4j installation instructions.
# 2025-06-26 15:15:23.517+0000 INFO  Logging config in use: File 'D:\neo4j-community-2025.05.0\conf\user-logs.xml'
# 2025-06-26 15:15:23.527+0000 INFO  Starting...
# WARNING: A terminally deprecated method in sun.misc.Unsafe has been called
# WARNING: sun.misc.Unsafe::objectFieldOffset has been called by org.jctools.util.UnsafeAccess (file:/D:/neo4j-community-2025.05.0/lib/jctools-core-4.0.5.jar)
# WARNING: Please consider reporting this to the maintainers of class org.jctools.util.UnsafeAccess
# WARNING: sun.misc.Unsafe::objectFieldOffset will be removed in a future release
# 2025-06-26 15:15:24.618+0000 INFO  This instance is ServerId{c9cff1a8} (c9cff1a8-7b84-44d9-ac13-1ce8ebd4ed8f)
# 2025-06-26 15:15:25.506+0000 INFO  ======== Neo4j 2025.05.0 ========
# 2025-06-26 15:15:30.173+0000 INFO  Anonymous Usage Data is being sent to Neo4j, see https://neo4j.com/docs/usage-data/
# 2025-06-26 15:15:31.449+0000 INFO  Bolt enabled on localhost:7687.
# 2025-06-26 15:15:33.442+0000 INFO  HTTP enabled on localhost:7474.
# 2025-06-26 15:15:33.444+0000 INFO  Remote interface available at http://localhost:7474/
# 2025-06-26 15:15:33.454+0000 INFO  id: 9551E12259B3EA4183495ECC3F31950859EC9BD92350C3DB15043765541020AF
# 2025-06-26 15:15:33.456+0000 INFO  name: system
# 2025-06-26 15:15:33.457+0000 INFO  creationDate: 2025-06-26T15:15:28.806Z
# 2025-06-26 15:15:33.458+0000 INFO  Started.

# 修改密码：neo4j -> Zrp031030

# 3.启动软件
# 1.控制台启动
# 进入bin目录，当前目录启动终端，执行以下命令：neo4j console
# 缺点：控制台终端关系，服务就停止了
# 2.将neo4j安装为服务
# 安装为服务之后，就可以后台运行了，关闭终端窗口，服务也能正常使用。
# Windows系统：
# neo4j.bat windows-service install
# neo4j.bat windows-service uninstall

# PS D:\neo4j-community-2025.05.0\bin> neo4j install-service
# neo4j : 无法将“neo4j”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正
# 确，然后再试一次。
# 所在位置 行:1 字符: 1
# + neo4j install-service
# + ~~~~~
#     + CategoryInfo          : ObjectNotFound: (neo4j:String) [], CommandNotFoundException
#     + FullyQualifiedErrorId : CommandNotFoundException


# Suggestion [3,General]: 找不到命令 neo4j，但它确实存在于当前位置。默认情况下，Windows PowerShell 不会从当前位置加载命令。如果信任此命令，请改为键入“.\neo4j”。有关详细信息，请参阅 "get-help about_Command_Precedence"。
# PS D:\neo4j-community-2025.05.0\bin> .\neo4j install-service
# .\neo4j : 无法加载文件 D:\neo4j-community-2025.05.0\bin\neo4j.ps1，因为在此系统上禁止运行脚本。有关详细信息，请参阅 htt
# ps:/go.microsoft.com/fwlink/?LinkID=135170 中的 about_Execution_Policies。
# 所在位置 行:1 字符: 1
# + .\neo4j install-service
# + ~~~~~~~
#     + CategoryInfo          : SecurityError: (:) []，PSSecurityException
#     + FullyQualifiedErrorId : UnauthorizedAccess
# PS D:\neo4j-community-2025.05.0\bin> neo4j.bat install-service
# neo4j.bat : 无法将“neo4j.bat”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确
# 保路径正确，然后再试一次。
# 所在位置 行:1 字符: 1
# + neo4j.bat install-service
# + ~~~~~~~~~
#     + CategoryInfo          : ObjectNotFound: (neo4j.bat:String) [], CommandNotFoundException
#     + FullyQualifiedErrorId : CommandNotFoundException


# Suggestion [3,General]: 找不到命令 neo4j.bat，但它确实存在于当前位置。默认情况下，Windows PowerShell 不会从当前位置加载命令。如果信任此命令，请改为键入“.\neo4j.bat”。有关详细信息，请参阅 "get-help about_Command_Precedence"。
# PS D:\neo4j-community-2025.05.0\bin> .\neo4j.bat install-service
# Unmatched argument at index 0: 'install-service'
# Did you mean: neo4j windows-service install or neo4j windows-service uninstall or neo4j windows-service?
# PS D:\neo4j-community-2025.05.0\bin> .\neo4j.bat windows-service install
# WARNING: A terminally deprecated method in sun.misc.Unsafe has been called
# WARNING: sun.misc.Unsafe::objectFieldOffset has been called by org.jctools.util.UnsafeAccess (file:/D:/neo4j-community-2025.05.0/lib/jctools-core-4.0.5.jar)
# WARNING: Please consider reporting this to the maintainers of class org.jctools.util.UnsafeAccess
# WARNING: sun.misc.Unsafe::objectFieldOffset will be removed in a future release
# WARNING! You are using an unsupported Java runtime.
# * Please use Java(TM) 21 to run Neo4j.
# * Please see https://neo4j.com/docs/ for Neo4j installation instructions.
# Neo4j service installed.
# PS D:\neo4j-community-2025.05.0\bin> .\neo4j.bat start
# WARNING: A terminally deprecated method in sun.misc.Unsafe has been called
# WARNING: sun.misc.Unsafe::objectFieldOffset has been called by org.jctools.util.UnsafeAccess (file:/D:/neo4j-community-2025.05.0/lib/jctools-core-4.0.5.jar)
# WARNING: Please consider reporting this to the maintainers of class org.jctools.util.UnsafeAccess
# WARNING: sun.misc.Unsafe::objectFieldOffset will be removed in a future release
# Directories in use:
# home:         D:\neo4j-community-2025.05.0
# config:       D:\neo4j-community-2025.05.0\conf
# logs:         D:\neo4j-community-2025.05.0\logs
# plugins:      D:\neo4j-community-2025.05.0\plugins
# import:       D:\neo4j-community-2025.05.0\import
# data:         D:\neo4j-community-2025.05.0\data
# certificates: D:\neo4j-community-2025.05.0\certificates
# licenses:     D:\neo4j-community-2025.05.0\licenses
# run:          D:\neo4j-community-2025.05.0\run
# Starting Neo4j.
# Started neo4j. It is available at http://localhost:7474
# There may be a short delay until the server is ready.

# 3.启动、停止、重启、查询
# .\neo4j.bat start
# .\neo4j.bat stop
# .\neo4j.bat restart
# .\neo4j.bat status

# 4.访问数据库
# 浏览器访问：http://localhost:7474
# Py2neo访问：neo4j://localhost:7687

# 5.切换数据库
# D:\neo4j-community-2025.05.0\conf\neo4j.conf
# initial.dbms.default_database=xxx