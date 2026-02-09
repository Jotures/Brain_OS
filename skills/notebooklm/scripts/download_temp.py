import requests
import sys
import os

url = "https://prod-files-secure.s3.us-west-2.amazonaws.com/ecb567f5-8527-46bb-b364-adb299b07bea/d5166ac9-9966-422c-be57-2150092b8241/krugman-2013-fundamentos-de-economc3ada.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466S4DEUWWU%2F20260206%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260206T205134Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEIX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIHvU02Q1GPNNqPdZxrMKwEe0Bm6Yqt0u%2FK47LFbKo1kQAiEA8Bx13t4cBJ3Ef3Ho0pEofXU1I0rAE%2BvDe6ibgT1g9csq%2FwMIThAAGgw2Mzc0MjMxODM4MDUiDIb6BzB3uJsWldcg6CrcAy0Adl%2F7uCmzAXIuYJiSAAXMVa9%2BUY22%2F4H7VNWoCJwA3BD2NmPWKFu0VBLu3Q5s6RTve%2F0Roa2yiUaEpI2046%2FhuaViX7rQZ0QLHoKbDYEyERRzR6u1oPKjj6U6%2F854Ha8iG0NrapvY9PyXNS1LnZahYPSxjxqOsL5p5WRZzMNdpQnxTyu%2BJILUujxob1kjqqckNqB%2FUVE%2ByygpT7KtviIF9DNScIudn2aCNZ2DhR7JQXDkMHp4c69n23xsoVlxs40ss2q1uRWH%2Fo2t21OTfgtsPnkIArfdKNgzSsj4eiUTPVUIG6CugUXVWmNmIZCkVeKVQ68r1YKUKYlATVTBRlaE5vo9Vm1f4Zuo7AMHouXBBiFYB8LNPlhtFd5rUr%2BLRBtf%2FlSkA5Jx8EKdqNziJUmG318nFn0Yu2lE5Oym86xkH5UcakSSf5t8Wr6yHhSVdXkP1Ui0N0xaShcmCOy118gYWcL0EzJIv2UVvxA9lCAzIfxxiZYUCxbMs3T1AED%2Fe8VM%2BXvum78TYdOTpqABP%2BpB0yM6mXNISzTGzdUUxXr5QYqKIzd1O6NCcgq4HZtq9FRKwrhb3PoWm9x2ecRIOSaovUc6mJoSOv3Q7x0hONR80PS8TEidYxqxxQgBMPyhmcwGOqUBc3IcSafJeA2eX15atDDYeIzYC4aar23z6dUE01B79tL59cY9gORpomqlHYALbsDZqXEQZCRABxZz39TH33EFSPAiBzvS%2BOLZGhQ%2F9DN7cDCTUdm7ise9MQbiSYBzErLSGNUuGkmXTwpCujYB3PV6XXPpD04q%2Fh0DE0Aco4qaBdGYQGtxyUgIYMPsmc4wRE5tdXxmYKaQkJwb0CrEC4raJ%2B6HfIjo&X-Amz-Signature=5c2c2292323d5bb403d5c9340e737e28fa6b23bd1f71bf3588bfd72f70ebec7a&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject"
output_path = r"c:\Users\Ruben J\Documents\Antigravito Proyects\Brain_OS\carrera\semestres\2026-1\cursos\03_economia_gestion_publica\recursos\krugman-2013-fundamentos.pdf"

os.makedirs(os.path.dirname(output_path), exist_ok=True)

print(f"Downloading to {output_path}...")
response = requests.get(url, stream=True)
if response.status_code == 200:
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Download complete.")
else:
    print(f"Failed to download. Status code: {response.status_code}")
