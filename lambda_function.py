import sys, os, json

libLocaion = str(os.getcwd()) + "/lib"
sys.path.append(libLocaion)
#sys.path.append('/var/task/.requirements')


#from flask import Flask


import multiprocessing
#from multiprocessing import Process, Pool
from multiprocessing import Process, Pipe
#import time
#import requests
#import sys

try:
  import boto3
except:
  print("Error: import boto3")
  print(str(sys.exc_info()))
  sys.exit(1)



def get_all_region(use_profile=True):
  try:
    use_profile = os.environ.get("use_profile")
    profile_name = os.environ.get("profile_name")
    if use_profile == "Y":
      session = boto3.Session(profile_name=profile_name)
      ec2_client = session.client('ec2', region_name='ap-south-1')
    else:
      ec2_client = boto3.client('ec2', region_name='ap-south-1')
  except:
    print("Error: ec2_client get_all_region")
    print(str(sys.exc_info()))
    sys.exit(1)


  ec2_regions = []
  try:
    ec2_regions_res = ec2_client.describe_regions()
    for region in ec2_regions_res['Regions']:
      ec2_regions.append(region['RegionName'])
  except:
    print("Error: describe_regions")
    print(str(sys.exc_info()))
    sys.exit(1)
  return ec2_regions

def get_instances(ec2_region,return_dict):
  try:
    use_profile = os.environ.get("use_profile")
    profile_name = os.environ.get("profile_name")
    if use_profile == "Y":
    #  print("profile")
      session = boto3.Session(profile_name=profile_name)
      ec2_client = session.client('ec2', region_name=ec2_region)

    else:
     # print("Role")
      ec2_client = boto3.client('ec2', region_name=ec2_region)
  except:
    print("Error: ec2_client get_instances")
    print(str(sys.exc_info()))
    sys.exit(1)

  ec2_instances = []
  try:
    ec2_instances_res = ec2_client.describe_instances()
    for reservation in ec2_instances_res['Reservations']:
      for instance in reservation['Instances']:
        ihash = {}
        ihash['instance-id'] = instance['InstanceId']
        ihash['instance-type'] = instance['InstanceType']
        ihash['region'] = ec2_region
        ihash['state'] = instance['State']['Name']
        ec2_instances.append(ihash)
    #return ec2_instances
    return_dict[ec2_region] = ec2_instances
    #final_hash[ec2_region] = ec2_instances
    #print(ec2_instances)
  except:
    print("Error: describe_instances get_instances")
    print(str(sys.exc_info()))
    sys.exit(1)

#app = Flask(__name__)
#@app.route("/")
def main_func(*arg):
  ec2_regions = get_all_region()
  manager = multiprocessing.Manager()
  return_dict = manager.dict()
  processes = []
  for ec2_region in ec2_regions:
    process = Process(target=get_instances, args=(ec2_region,return_dict))
    processes.append(process)
  for process in processes:
    process.start()
  for process in processes:
    process.join()
  final_list = []
  for i in return_dict.values():
    final_list.extend(i)
  final_hash = {}
  final_hash['statusCode'] = 200
  final_hash['headers'] = {"Content-Type": "application/json"}
  final_hash['body'] = json.dumps(final_list)

  return final_hash

  # pool = Pool(processes=(len(ec2_regions) + 1))
  # results = pool.map(get_instances, ec2_regions)
  # final_list = []
  # for i in results:
  #     final_list.extend(i)
  # return final_list




