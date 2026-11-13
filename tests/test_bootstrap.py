"""Offline bootstrap integration invariants; cfn-lint is a separate required check."""
import re
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class Bootstrap(unittest.TestCase):
    def test_batch_zero_capacity_and_output(self):
        s = (ROOT / 'deploy/batch.yaml').read_text()
        self.assertRegex(s, r'MaxVcpus:\s+Type: Number\s+Default: 16\s+MinValue: 0')
        self.assertIn('WorkerComputeArn:', s)
        self.assertIn('MinvCpus: 0', s)

    def test_network_ssm_and_roles(self):
        s = (ROOT / 'deploy/bootstrap.yaml').read_text()
        for expected in ['AWS::EC2::VPC', 'AWS::EC2::NatGateway', 'AWS::EC2::VPCEndpoint',
                         'AmazonSSMManagedInstanceCore', 'ecs-tasks.amazonaws.com',
                         'AmazonEC2ContainerServiceforEC2Role', 'ExistingBatchServiceRoleArn',
                         'RunnerProfileName', 'ResourceSignal:', 'HttpTokens: required']:
            self.assertIn(expected, s)
        self.assertNotIn('SecurityGroupIngress:', s)
        self.assertNotIn('FromPort: 22', s)
        self.assertNotIn('KeyName:', s)
        self.assertEqual(s.count('MapPublicIpOnLaunch: false'), 3)
        for output in ['VpcId', 'PrivateSubnets', 'BatchServiceRoleArn', 'InstanceProfileArn',
                       'JobRoleArn', 'JobRoleName', 'ExecutionRoleArn', 'ControllerId']:
            self.assertIn('  ' + output + ':', s.split('Outputs:')[1])

    def test_pinned_bootstrap_and_fail_closed(self):
        s = (ROOT / 'deploy/bootstrap.yaml').read_text()
        for expected in ['Python-3.11.11.tgz', 'NXF_VER=26.10.3', 'nf-amazon@3.12.1',
                         'java-21-amazon-corretto-headless', 'set -Eeuo pipefail',
                         'cfn-signal -e $?', 'BOOTSTRAP_OK', 'test', 'ap-southeast-1']:
            self.assertIn(expected, s)
        self.assertNotIn('batch:SubmitJob', s)  # Initial controller is SSM-only.
        self.assertNotIn('s3:*', s)  # Run-scoped access comes from existing runner stack.
        self.assertIn('UseRunnerProfile, !Ref RunnerProfileName, !Ref ControllerProfile', s)

if __name__ == '__main__':
    unittest.main()
