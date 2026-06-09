import cv2
import random
import time
import cvzone
from cvzone.HandTrackingModule import HandDetector

# 1. 初始化攝影機與偵測器
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)

# 2. 遊戲變數設定
timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [玩家分數, 電腦分數]
comNumber = 0
playerNumber = 0
resultText = ""

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1) # 鏡像畫面
    
    # 偵測手部（但不顯示預設的綠色骨架，我們自己畫比較高級）
    hands, img = detector.findHands(img, draw=True, flipType=False)
    
    if startGame:
        if stateResult is False:
            # 計算倒數時間 (從 3 秒開始)
            timer = time.time() - initialTime
            cv2.putText(img, f"{int(4-timer)}", (600, 400), cv2.FONT_HERSHEY_PLAIN, 10, (0, 255, 255), 10)
            
            # 倒數時間到（超過 3 秒）
            if timer > 3:
                stateResult = True
                timer = 0
                
                # A. 判斷玩家出了多少 (算幾隻手指伸直)
                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    # fingersUp 會回傳長這樣 [0, 1, 1, 0, 0]，加總就是數字
                    playerNumber = sum(fingers)
                else:
                    playerNumber = 0 # 沒伸出手算 0
                
                # B. 電腦隨機出 0 到 5
                comNumber = random.randint(0, 5)
                
                # C. 比大小邏輯判定
                if playerNumber > comNumber:
                    scores[0] += 1 # 玩家得 1 分
                    resultText = "YOU WIN! :)"
                elif playerNumber < comNumber:
                    scores[1] += 1 # 電腦得 1 分
                    resultText = "YOU LOSE! :("
                else:
                    resultText = "DRAW! :O"

    # --- 畫面視覺視覺 UI 設計 (高級感的關鍵) ---
    
    # 1. 繪製得分板 (半透明科技感矩形)
    cv2.rectangle(img, (100, 20), (400, 100), (50, 50, 50), cv2.FILLED)
    cv2.rectangle(img, (880, 20), (1180, 100), (50, 50, 50), cv2.FILLED)
    cv2.putText(img, f"PLAYER: {scores[0]}", (120, 70), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
    cv2.putText(img, f"COM: {scores[1]}", (900, 70), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
    
    # 2. 如果開牌了，顯示雙方的數字與勝負
    if stateResult:
        # 顯示電腦出的數字
        cv2.putText(img, f"COM: {comNumber}", (920, 200), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 165, 255), 3)
        # 顯示玩家出的數字
        cv2.putText(img, f"YOU: {playerNumber}", (120, 200), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 200, 0), 3)
        
        # 顯示勝負大字（根據輸贏變換顏色）
        color = (0, 255, 0) if "WIN" in resultText else (0, 0, 255) if "LOSE" in resultText else (255, 255, 255)
        cv2.putText(img, resultText, (450, 360), cv2.FONT_HERSHEY_SYS, 2.5, color, 5)
        
        # 提示字緣
        cv2.putText(img, "Press SPACE to Play Again", (440, 650), cv2.FONT_HERSHEY_PLAIN, 2, (200, 200, 200), 2)

    else:
        if not startGame:
            cv2.putText(img, "Press SPACE to START", (430, 380), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 255, 0), 3)

    # 顯示主畫面
    cv2.imshow("Finger Number Battle", img)
    
    # 按鍵控制
    key = cv2.waitKey(1)
    if key == ord(' '): # 按空白鍵開始倒數或下一局
        startGame = True
        stateResult = False
        initialTime = time.time()
    elif key == ord('q'): # 按 q 離開
        break

cap.release()
cv2.destroyAllWindows()
