# 카카오 API 알림을 이용한 SMART CCTV 졸업작품

### 연구 배경
1. 연구 필요성
- 현재 CCTV 상황의 문제점과 사건에 대한 상황조치의 한계
- 1인 다수의 CCTV 관리의 한계와 신속한 문제 상황 대처 필요
2. 연구 목표
- 음성 및 영상 처리를 이용하여 특정 음성 또는, 화재를 감지하였을  경우 영상을 서버로 송신하여, 수신된 영상을 통해 담당자로부터 화재 및 범죄 상황에 대한 신속한 조치가 가능한 CCTV 설계

### 연구 내용
1. 작동 원리<br>
![image](https://user-images.githubusercontent.com/59759468/105460410-12e64a80-5ccf-11eb-99bb-7551911de9ef.png)

2. 블록도<br>
![image](https://user-images.githubusercontent.com/59759468/105460335-fd712080-5cce-11eb-8696-73cad70be642.png)

3. 흐름도
- 센서 제어장치 흐름도<br>
![image](https://user-images.githubusercontent.com/59759468/105460422-17126800-5ccf-11eb-89a8-25dd5f2e0775.png)
![image](https://user-images.githubusercontent.com/59759468/105460449-21346680-5ccf-11eb-9bc7-09d11f0b9cb4.png)
![image](https://user-images.githubusercontent.com/59759468/105460635-6fe20080-5ccf-11eb-8e8f-7fe384496d15.png)

- 카메라 제어장치 흐름도<br>
![image](https://user-images.githubusercontent.com/59759468/105460782-a3bd2600-5ccf-11eb-9810-6fb9329709a1.png)

4. 카메라 제어장치 설계 및 제작
- 하드웨어<br>
![image](https://user-images.githubusercontent.com/59759468/105460967-e7b02b00-5ccf-11eb-9bd4-81afc09fee32.png)

- 소프트웨어(Arduino)<br>
```
#include <Wire.h>
#include <SoftwareSerial.h> // 소프트웨어 Serial 통신 라이브러리 사용
#include <Adafruit_AMG88xx.h>
//#include <Keyboard.h>

SoftwareSerial VoiceModule(2, 3);

// 온도 센서
char temp_case = 0;
char chars[] = {'0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'F'};
Adafruit_AMG88xx amg;

float pixels[AMG88xx_PIXEL_ARRAY_SIZE];

// 가스 센서
char gas_case = 0; 
int gasPin = A0;

// 음성 인식
char voice_case = 0;
int voice_recogn = 0;

void setup()
{
  Serial.begin(9600); // 통신 속도 9600bps로 PC와 시리얼 통신 시작
  VoiceModule.begin(9600); // 통신 속도 9600bps로 모듈과 시리얼 통신 시작
  //Keyboard.begin();

  bool status = amg.begin();
  
  if (!status)
  {
    Serial.println("There's no Temparature Sensor.");
    while (1);
  }
  Serial.println("Temparature Sensor READY");
  
  delay(1000);
  
  VoiceModule.write(0xAA); // compact mode 사용
  VoiceModule.write(0x37);

  delay(1000);
  
  VoiceModule.write(0xAA); // 그룹1 음성 명령어 imported
  VoiceModule.write(0x21);

  Serial.println("Voice Sensor READY");

}

void loop()
{

    Serial.println("TEMPERATURE : ");

    amg.readPixels(pixels);
    int temp;
    int Tmin = 1000, Tmax = 0;
     
    for (int i = 1; i <= AMG88xx_PIXEL_ARRAY_SIZE; i++)
    {
      temp = pixels[i - 1] * 10;
      Tmin = Tmin > temp ? temp : Tmin;
      Tmax = Tmax < temp ? temp : Tmax;
    }
    
    Serial.print("[");
    
    for (int i = AMG88xx_PIXEL_ARRAY_SIZE; i >= 1; i--)
    {
      int temp = (pixels[i - 1] * 10);
      int idx = map(temp, Tmin, Tmax, 0, 21);
    
      if ( i % 8 == 0 ) 
      {
        Serial.println();
      }
      
      Serial.print(chars[idx]);
      Serial.print(", ");
      
      if (chars[idx] == 'F')
      {
        temp_case = 1;
      }
    }
    
    Serial.println("]");
    
    Serial.println();
    
    Serial.print("GAS : ");
    Serial.println(analogRead(gasPin));

    if (analogRead(gasPin) >= 600)
    {
      gas_case = 1;
    }
    
    Serial.println();
    
    Serial.print("VOICE INPUT : ");
    voice_recogn = VoiceModule.read();

    if(voice_recogn == 0x11)
    {
      Serial.println("YES"); // 
      voice_case = 1;
    }

    else if(voice_recogn == 0x12)
    {
      Serial.println("NO"); //아뇨
      voice_case = 1;
    }

    else if(voice_recogn == 0x13)
    {
      Serial.println("HELP"); //살려줘
      voice_case = 1;
    }

    else if(voice_recogn == 0x14)
    {
      Serial.println("FIRE"); //불이야
      voice_case = 1;
    }

    else if(voice_recogn == 0x15)
    {
      Serial.println("THEFT"); //도둑이야
      voice_case = 1;
    }

    else
    {
      Serial.println("No voice");
      voice_case = 0;
    }

    if(temp_case == 1 || gas_case == 1 || voice_case == 1)
    {
      //Keyboard.println("sh mjpg.sh");
      temp_case = 0;
      gas_case = 0;
      voice_case = 0;
    }

    delay(1000);
}
```
- 소프트웨어(Python)<
![image](https://user-images.githubusercontent.com/59759468/105462004-62c61100-5cd1-11eb-88ef-0a87ecf62960.png)
![image](https://user-images.githubusercontent.com/59759468/105462059-72455a00-5cd1-11eb-8718-44398f09161b.png)
![image](https://user-images.githubusercontent.com/59759468/105462095-80937600-5cd1-11eb-8ea2-9eeb009de417.png)
![image](https://user-images.githubusercontent.com/59759468/105462126-8ab57480-5cd1-11eb-8599-64e22c5ffa17.png)
![image](https://user-images.githubusercontent.com/59759468/105462143-8f7a2880-5cd1-11eb-87ca-0e6a5c92d059.png)

- 소프트웨어(django 서버 구축 및 Kakao API 사용자 알림 서비스)<br>
![image](https://user-images.githubusercontent.com/59759468/105461464-9bb1b600-5cd0-11eb-83f9-bb8661d46fdb.png)
![image](https://user-images.githubusercontent.com/59759468/105461467-9e141000-5cd0-11eb-8018-2f0ce3659886.png)
![image](https://user-images.githubusercontent.com/59759468/105461509-ab30ff00-5cd0-11eb-86ab-ff848b69fa66.png)
![image](https://user-images.githubusercontent.com/59759468/105461520-b1bf7680-5cd0-11eb-858b-3c1c91d49d4d.png)

