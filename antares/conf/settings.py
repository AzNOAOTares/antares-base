"""
Global configuration for Antares.
"""

## Database settings

db_host_local = 'localhost'
# db_host_remote = 'antd01.sdm.noao.edu'
db_host_remote = 'ant02.sdm.noao.edu' # interface to mysql cluster
db_user = 'root'
db_pwd = 'ant123ares'
# db_name = 'ANTARES'
db_name = 'antares_demo_d'

astro_db_host_remote = 'antdb01.sdm.noao.edu' # interface to mysql hosting astro catalogs
astro_db_user = 'root'
#astro_db_pwd = 'antareS'
astro_db_pwd = 'ant123ares'
# db_name = 'ANTARES'
astro_db_name = 'astro_catalog'
astro_db_port = 3308 # different with the default 3306 to avoid conflict with mysql cluster

path2metafile = '/home/vagrant/antares_meta.json'
#path2metafile = '/Users/shuoyang/antares_meta.json'

antaresPathPrefix = '/home/antares/nfs_share/'

Run_Local = 'local'
Run_Distributed = 'distributed'

Running_Mode = Run_Local # default option

## System settings
# Dashboard_Address = 'antdb01.sdm.noao.edu:8000'
Dashboard_Address = 'ant01.sdm.noao.edu:8000'

SSH_USERNAME = 'antares'

Watcher_IP = 'ant01.sdm.noao.edu'
#Watcher_IP = 'ant03.sdm.noao.edu'
#Watcher_IP = '128.196.3.196'
Watcher_Port = 7000

#Load_Balancer_IP = 'ant01.sdm.noao.edu'
Load_Balancer_IP = '128.196.3.196'
Load_Balancer_Port = 7700

# Controller_IPs = ['ant02.sdm.noao.edu', 'ant03.sdm.noao.edu', 'ant04.sdm.noao.edu',
#                  'ant05.sdm.noao.edu', 'antdb01.sdm.noao.edu']
# Controller_IPs = ['128.196.3.198', '128.196.3.200', '128.196.3.202',
#                   '128.196.3.204', '128.196.3.194']
Controller_IPs = ['128.196.3.198', '128.196.3.200', '128.196.3.202',
                  '128.196.3.204', '128.196.3.194', '128.196.3.196']
#Controller_IPs = ['ant01.sdm.noao.edu']

# The following are the same on each node
Controller_Port = 8001
Alert_Worker_Count = 16
Alert_Worker_Ports = [Controller_Port+1+i for i in range(Alert_Worker_Count)]
