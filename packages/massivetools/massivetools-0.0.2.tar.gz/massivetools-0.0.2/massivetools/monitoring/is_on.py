import subprocess
import requests
import time
import os
from CVutils.slack_api import  SLACK
import time
from typing import List

def get_gpu_process_ids_and_memory(utils):
    """nvidia-smi를 사용하여 현재 실행 중인 GPU 프로세스의 PID와 메모리 사용량을 각각의 리스트로 가져옵니다."""
    pids = []
    memory_usage = []

    if utils:
        # GPU 프로세스 ID와 사용 중인 메모리 크기를 가져옵니다.
        command = "nvidia-smi | grep 'python' | awk '{ print $5, $8 }'"
        process = subprocess.run(command, shell=True, text=True, capture_output=True)
        # Get the output and split it into a list of tuples
        results = process.stdout.strip().split('\n')
        for result in results:
            if len(result.split()) == 2:
                pid, memory = result.split()
                pids.append(int(pid))
                memory_usage.append(memory)
    else:
        # 이 부분은 PID와 메모리 사용량을 가져옵니다.
        result = subprocess.run(['nvidia-smi', '--query-compute-apps=pid,used_memory', '--format=csv,noheader,nounits'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8').strip().split('\n')
        for line in output:
            if ',' in line:
                pid, memory = line.split(',')
                pids.append(int(pid))
                memory_usage.append(memory.strip())
        
    return pids, memory_usage

def get_command(pid):
    # Define the command to be executed
    command = f"ps -ef | grep {pid} | awk '{{for(i=8; i<=NF; i++) printf $i \" \"; print \"\"}}' | head -n 1"

    # Execute the command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Get the standard output and error
    stdout, stderr = process.communicate()

    # Decode the byte string to a regular string (assuming default system encoding)
    output_str = stdout.decode()

    # Print or use the output string
    return output_str
    
def is_pid_running(pid):
    """주어진 PID의 프로세스가 실행 중인지 확인합니다."""
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True




def main():
    checked_pids = set()
    pid_memory_mapping = {}  # PID와 메모리 사용량을 매핑하기 위한 딕셔너리
    slack = SLACK()

    while True:
        current_pids, GPU_memories = get_gpu_process_ids_and_memory(utils=True)
        
        # 현재 PID와 메모리 사용량을 매핑합니다.
        for pid, memory in zip(current_pids, GPU_memories):
            if pid not in checked_pids:
                checked_pids.add(pid)
            pid_memory_mapping[pid] = memory  # 메모리 정보를 업데이트 또는 추가합니다.
        
        # 체크된 PID 리스트를 순회하면서 실행되지 않는 프로세스를 찾습니다.
        for pid in list(checked_pids):
            if not is_pid_running(pid): #프로세스가 존재하는지 확인
                
                # message = get_command(pid)
                memory_usage = pid_memory_mapping.get(pid, "Unknown")  # PID에 해당하는 메모리 사용량을 가져옵니다.
                print(f"Process with PID {pid} (used memory: {memory_usage}) is no longer running.")
                message = slack.create_block("#36a64f",
                                             "Important Alert!",
                                             f"Process with PID {pid} (used memory: {memory_usage}) is no longer running.")
                slack.send_message("monitoring", message)
                checked_pids.remove(pid)
                if pid in pid_memory_mapping:
                    del pid_memory_mapping[pid]  # 더 이상 사용되지 않는 PID를 매핑에서 제거합니다.
        
        time.sleep(1)  # 60초마다 확인

if __name__ == "__main__":
    main()