# プロジェクト演習Ⅰ・テーマD
## 第六回
### ゲームの説明、機能
- 緑色の蛇をキーで操作して、foodを食べ成長させていくゲーム
- foodに接触すると自身の速度と大きさ、点数が増加され難易度が上がっていく
- enemyに接触すると自身の速度と大きさ、点数が減少される
- foodは明るい赤色、enemyは暗い赤色
- foodまたはenemyに当たると両方ともランダムに再配置される
- 壁に当たるとgameoverになり点数とretryボタンが表示される
- retryボタンはマウスクリックで押せる
####　エフェクトなどについて
- 背景の四角形がsnakeの動く方とは逆に動かすことでスクロールさせている
- 背景の四角形の色をランダムに設定しちかちかさせている
- foodを食べた際は破片が飛び散るようにした
- enemyに触れた際は遅延させることによってダメージを食らっていることを認識できるようにした
##### to do
- HPバーを作りenemyに三回当たったらgameoverなどの使用を追加したい
- マリオでいうファイヤーフラワーのようなアイテムなどの機能を追加してみたい

### c0b21084 マージ
- プレイ中もスコアを表示