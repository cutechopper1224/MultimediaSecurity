首先因為檔案有點大，請將檔案解壓縮後，將rawTexts資料夾內的所有文本解壓縮，建一個叫做rawText的資料夾丟進名稱為dataowner的資料夾裡面。
（也可以不要用所有的文本，但必須在程式中進行設定）

接著執行該資料夾底下的create.py，生成加密後的原始文件。加密過程會需要設定data owner的個人密碼，可以隨意輸入。

設定完成後就可以在根目錄打開主程式main.py：

plaintext 搜尋：

先在關鍵字欄輸入語法，調整在右下方的最大搜尋數目
(必須小於1000），再按「搜尋」 鍵，從左邊的列表即會出現搜尋結果。

語法如下：

keyword1:modifier keyword2:modifier ...

keyword是 keyword.txt內包含的文字，目前只可以用關鍵字進行搜尋。

modifier是要搜尋的關鍵字出現在哪個地方。title是標題，content是內文，push是推文。all代表沒有限制。

範例如下：
主角:title 巨人:content 劇情:push
代表要搜尋「主角」出現在標題、「巨人」出現在內文、「劇情」出現在推文的所有文章，並依照吻合程度由高至低回傳搜尋結果。

回傳結果是會加密過的文件，此時需要按「解密」鈕才能看到明文。解密的過程會要求輸入密碼，密碼必須和前面加密時所用的吻合。


UDMRS

和plaintext搜尋一樣的關鍵字輸入方式，但是改成透過按下「安全搜尋」進行查詢

只能對資料庫中第99001-100000筆資料(1000筆)資料進行查詢。

一些實驗數據：
(1000筆)
BuildingIndex: 4.347467秒
搜尋
(1個關鍵字): 
k=5: 0.776389秒
k=10: 0.804485秒
k=20: 0.780666秒
k=50: 0.782318秒

(5個關鍵字): 
k=5: 0.913023秒
k=10: 0.785530秒
k=20: 1.052195秒
k=50: 0.838183秒


BDMRS:

Step1: 到create.py生成dataowner的secret和BDMRS secure index
Step2: 輸入keyword->filename當成關鍵字，然後按下「產生trapdoor」。
例如：主角:all 魔法:all->magic
則會在trapdoor資料夾生成檔名為magic的trapdoor。
如不指定檔名，請使用和前面一樣的查詢方式，檔名將自動設為trapdoor。
Step3:輸入檔案名稱當成關鍵字，然後按下「使用Trapdoor查詢」，如：magic。
如想要使用預設的trapdoor，請留白。
Step4:回傳結果是會加密過的文件，此時需要按「解密」鈕才能看到明文。解密的過程會要求輸入密碼，密碼必須和前面加密時所用的吻合。


一些實驗數據：
(1000筆)
BuildingIndex: 4.618314秒

搜尋
(1個關鍵字): 
建立Trapdoor: 2.335814秒
搜尋：約 1.5秒

(5個關鍵字): 
建立Trapdoor: 1.953600秒
搜尋：約 1.5秒


#TODO
EDMRS
(Optional) Other Architecture

如要新增新的按鈕或調整介面，使用qtdesigner生成.ui檔，覆蓋掉想要變更的.ui檔案即可。

