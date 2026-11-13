"""Render reviewable CloudFormation from generated policy fragments; does not contact AWS."""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--policies',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(); policies=json.loads(a.policies.read_text())
t={'AWSTemplateFormatVersion':'2010-09-09','Description':'Separate research runner; never alters frozen controller deny policy',
'Parameters':{'JobRoleName':{'Type':'String'}},'Resources':{
'RunnerRole':{'Type':'AWS::IAM::Role','Properties':{'ManagedPolicyArns':[{'Fn::Sub':'arn:${AWS::Partition}:iam::aws:policy/AmazonSSMManagedInstanceCore'}],'AssumeRolePolicyDocument':{'Version':'2012-10-17','Statement':[{'Effect':'Allow','Principal':{'Service':'ec2.amazonaws.com'},'Action':'sts:AssumeRole'}]},'Policies':[{'PolicyName':'ResearchRun','PolicyDocument':policies['controller']}]}},
'RunnerProfile':{'Type':'AWS::IAM::InstanceProfile','Properties':{'Roles':[{'Ref':'RunnerRole'}]}},
'JobWorkPolicy':{'Type':'AWS::IAM::Policy','Properties':{'PolicyName':{'Fn::Sub':'${AWS::StackName}-DimpleRunWorkPrefix'},'Roles':[{'Ref':'JobRoleName'}],'PolicyDocument':policies['worker_job']}}},
'Outputs':{'RunnerProfileArn':{'Value':{'Fn::GetAtt':['RunnerProfile','Arn']}},'RunnerRoleArn':{'Value':{'Fn::GetAtt':['RunnerRole','Arn']}}}}
with a.output.open('x') as f:json.dump(t,f,indent=2)
