IOTA:【技術解説】MAMとは。IOTAのIoT性。
　投稿して初めて気づいたが右の目次にスクロールバーがついている。こんなのは初めてだ。記事が長いのでササっとMAMの簡単なことを理解したい人もいると思うので記事の概要を示す。
>1. MAMの機能面だけ知りたい人 - 「旧MAMと新MAM」の「チャンネルのタイプ」まで
>2. MAMの大まかな技術まで知りたい人 - 「実装のイメージ」の「メッセージチェーン」まで
>3. 深くまで知りたい人 - 全部


# はじめに
　MAM（Masked Authenticated Message）は開発中の機能である。現在、MAMの[最新バージョン](https://github.com/iotaledger/MAM)は[Rust](https://github.com/iotaledger/iota.rs)で開発が進められている。本記事はそんなMAMの[JavaScript](https://github.com/iotaledger/iota.lib.js)で開発された[旧バージョン](https://github.com/iotaledger/mam.client.js)を説明したものである。旧バージョンであるため、実際にIOTAで実装されるMAMとは少しの違いが出てくるのは必死だが、大枠とアルゴリズムを理解するためには問題ないと判断した。

## IOTA（アイオータ）とは
おなじみ初心者向けの解説サイトを念のためここに列挙しておく。
>[**IOTA日本語ファンサイト**](https://iotafan.jp/)　実質IOTA日本公式サイト。というのもIOTA公式の情報を日本語訳して掲載しているからである。初心者向けの情報も多く掲載されている。
>[**レオンハルトジャパン公式BLOG**](http://lhj.hatenablog.jp/entry/iota)　日本におけるIOTAの最古参。様々なサイトのリンクが紹介されているため、ここを拠点に掘り下げていくといい。

>**ホワイトペーパー**[英語](https://www.dropbox.com/s/i4l3g88wh6gpi5d/IOTA_Whitepaper%20v1.1.pdf?dl=0) [日本語](https://www.dropbox.com/s/1w5vtu7s4idquc9/IOTA_Whitepaper%20v1.1%20in%20Japanese.pdf?dl=0)　Tangleについての概要は序盤までで、それ以降は安全性、想定される攻撃とその耐性について高度な数学で説明している。後半は初心者向きではない。

>[**Redditの初心者向けスレッド（英語）**](https://www.reddit.com/r/Iota/comments/61rc0c/for_newcomers_all_information_links_you_probably/)　僕はここから始まった。

>[**IOTA Guide（英語）**](https://domschiener.gitbooks.io/iota-guide/content/)　ホワイトペーパーが理学部なら、これは工学部。

# MAM
　MAMはMasked Authenticated Messageの略である。いい訳語が浮かばないので砕いて説明する。IOTAの送金は手数料がかからない。また、送金Bundle生成の際、`Transaction`オブジェクトの`signatureFragment`に任意のメッセージを貼り付けることができた\*ことを思い出して欲しい[\*解説](https://qiita.com/ABmushi/items/0c9f73e08fdb6597ab9c#%E5%87%BA%E5%8A%9B%E9%83%A8---output) 。MAMはそのメッセージを暗号化することで秘匿性を持たせ、Tangleを分散型クラウド記憶領域として使えるようにする機能だ。
　各Seed所有者が主張できる記憶領域のことをMAMでは**チャンネル(Channel)**と呼ぶ。
　また、そのチャンネルを閲覧するための鍵を**チャンネル鍵（Channel Key）**と呼ぶ。チャンネルを公開したければチャンネル鍵を公開すれば良いし、公開したくなければチャンネル鍵を誰にも教えなければ良い。チャンネル鍵は任意に投稿者が決めて良い。
　チャンネルに投稿されたメッセージは、Tangle上の**アドレスに保存されている**と考えられる。[iota search](https://iotasear.ch/)でアドレス検索をするのと同じようにメッセージを閲覧できる。もし、チャンネル鍵があればそのメッセージを理解できる。

## MAMとは
　MAMはよくラジオに例えられる。周波数を知る人だけがラジオの番組を聞くことができるように、**チャンネル鍵**を知っている者だけが該当のチャンネルを閲覧できる。
ポイントは以下の通り。
>1. メッセージをチャンネル鍵で**暗号化**して投稿する。
>2. チャンネル鍵を知っている人のみがチャンネルのメッセージを**復号化**して中身を理解できる。
>3. チャンネル鍵を知っているだけではチャンネルの所有者にはなれない（=投稿はできない）。投稿するには結局**Seed**が必要である。
>4. チャンネル内でメッセージは一歩通行に古い順から鎖のように保存される。（分裂もできる。）
>5. 鎖の途中から閲覧しても過去のメッセージに遡ることはできない。

詳しい技術は後半で説明する。

### 実用例
主な利用例として考えられるのが、例えば
>1. **IoTのデータ管理**：工場内のデバイスやセンサー群から集まった秘匿にしたい数値を暗号化してチャンネルに投稿し、担当者のみがもつChannel Keyでデータにアクセスする。生データの秘匿性を確保しつつ公開台帳に情報を保持できる。
>2. **グループチャット**：Channel Keyを教え合って２つ以上のチャンネル間をまたいでチャットする。（非公式Alpha版[iota1k](https://github.com/xx10t4/iota1k)が有志によって開発されている。）

## 旧MAMと新MAM
　旧MAMと新MAMというのは単純にバージョンが違うMAMである。[javascript](https://github.com/iotaledger/mam.client.js)で開発されていた旧MAMが現在では[Rust](https://github.com/iotaledger/MAM)開発に移行した。最新のMAMについては[*Introducing Masked Authenticated Messaging*](https://blog.iota.org/introducing-masked-authenticated-messaging-e55c1822d50e)という記事から概要は発表されている。
　ただ、機能だけ見れば上で説明したのと大差ない。大きな変更点を挙げるなら、新MAMではチャンネルのセキュリティの段階を設けて、用途に合わせて下記のような違うタイプのチャンネルを作れる。
　
###チャンネルのタイプ
>**Public（公開）**：保管されたメッセージはアドレスを使って復号。（アドレス自身が復号に使われるため、アドレスが分かればメッセージも見れる。）
**Private（非公開）**：`アドレス＝hash(root)`。**rootを使って復号**。（アドレスはハッシュ化されており、ハッシュ化前の生`root`を知っていないと、例えアドレスにアクセスしてもそのメッセージを復号できない。）
**Restricted（限定公開）**：`アドレス＝hash(root+key)`。**root+keyを使って復号**。（rootを教えることはPrivateチャンネルを公開することになるため、あくまでroot+keyを限定公開する。そのroot+keyを知っている人だけがRestrictedチャンネルにアクセスしてメッセージを復号できる。）

　旧MAMでもチャンネル鍵の公開の仕方で同じことをできるが、新MAMではそれをソフトウェア側がやってくれる。
　また、新MAMではチャンネル鍵という言葉を使わなくなった。その代わりSeedから生成される`Merkle root`という概念を使ってメッセージの暗号化・復号化する。

# MAMの実装
　本記事で今後MAMとはjavascriptで開発されていた旧MAMのことを指していると思っていただきたい。一度ざっとどうやってMAMが投稿され閲覧されるかの流れを見て欲しい。
## MAMの投稿 - post.js
[ソースコード](https://github.com/iotaledger/mam.client.js/blob/master/examples/post.js)

```js:post.js
const IOTA = require('iota.lib.js');
const MAM = require('../lib/mam');
const MerkleTree = require('../lib/merkle');
const Encryption = require('../lib/encryption');
var Crypto = require('iota.crypto.js');

const iota = new IOTA({
  provider: 'http://localhost:14600'
});

//  シード
const seed = 'PAUL9NOZTUVHPBKLTFVRJZTOPODGTYHRUIACDYDKRNAQMCUZGNWMDSDZMPWHKQINYFPYTIEDSZ9EJZYOD';

//  投稿したいメッセージ
const message = "\"'I'm still here for IOTA in the same way that you're here for me, each person is an intricate piece of infinity. -Eyedea\" - Dukakis";

//  チャンネル鍵の生成。
const channelKeyIndex = 3;
const channelKey = Crypto.converter.trytes(Encryption.hash(Encryption.increment(Crypto.converter.trits(seed.slice()))));

//  Merkle Tree生成に必要（後述）  
const start = 3;
const count = 4;    // Merkle Treeのsize
const security = 1;

//  Merkle Treeを２つ生成
const tree0 = new MerkleTree(seed, start, count, security);
const tree1 = new MerkleTree(seed, start + count, count, security);
let index = 0;

//  MAM投稿に必要なBundleを生成
const mam = new MAM.create({
    message: iota.utils.toTrytes(message),  // messageをトライトに変換
    merkleTree: tree0,
    index: index,
    nextRoot: tree1.root.hash.toString(),
    channelKey: channelKey,
});

// Depth
const depth = 4;

// minWeighMagnitude
const minWeightMagnitude = 13;

console.log("Next Key: " + mam.nextKey);

// Send trytes（Bundleを送信）
iota.api.sendTrytes(mam.trytes, depth, minWeightMagnitude, (err, tx) => {
  if (err)
    console.log(err);
  else
    console.log(tx);
});

```
## MAMの閲覧 - getMessage.js
[ソースコード](https://github.com/iotaledger/mam.client.js/blob/master/examples/getMessage.js)

```js:getMessage.js
const IOTA = require('iota.lib.js');
const MAM = require('../lib/mam');
const MerkleTree = require('../lib/merkle');
const Encryption = require('../lib/encryption');
var Crypto = require('iota.crypto.js');

const iota = new IOTA({
  provider: 'http://localhost:14600'
});

//  シード
const seed = 'PAUL9NOZTUVHPBKLTFVRJZTOPODGTYHRUIACDYDKRNAQMCUZGNWMDSDZMPWHKQINYFPYTIEDSZ9EJZYOD';
const channelKeyIndex = 3;

//  チャンネル鍵の生成。（自分のチャンネルを閲覧する場合）
//  他人のチャンネルを閲覧する場合は生成せず、
//  単純に教えてもらったチャンネル鍵を代入。
const channelKey = Crypto.converter.trytes(Encryption.hash(Encryption.increment(Crypto.converter.trits(seed.slice()))));

//  Merkle Tree生成に必要（後述）
const start = 3;
const count = 4;    // Merkle Treeのsize
const security = 1;

//  Merkle Tree生成
const tree0 = new MerkleTree(seed, start, count, security);

//  rootを得る。
const root = tree0.root.hash.toString();



iota.api.sendCommand({
    command: "MAM.getMessage",
    channel: MAM.messageID(channelKey)
}, function(e, result) {
    if(e == undefined) {
        result.ixi.map(mam => {
            const output = MAM.parse({key: channelKey, message: mam.message, tag: mam.tag});
            const asciiMessage = iota.utils.fromTrytes(output.message);
            if (root === output.root) {
                console.log("Public key match for " + root);
            }
            console.log("received: " + asciiMessage);
        });

    }
});

```
# MAMの裏側 - 概要
## チャンネル鍵 - channelKey
　`chennelKey`は81トライトの任意のトライトだ。seedと同じである。まず、投稿者はチャンネルの最初の`message`を投稿する。`message`はこのチャンネル鍵を使って暗号化する。こうすることで、投稿者以外は`message`を理解することができない。なぜなら`message`の復号には`channelKey`が必要だからだ。

![mam_channelKey_basic.png](https://qiita-image-store.s3.amazonaws.com/0/187795/1459dbff-a02b-fc6c-bdb9-1caaa89844c7.png)

　しかし、これだと投稿を一回したらおしまいである。言い換えると、`chennelKey`１つにつき１つのメッセージしか管理できない。もし新しい投稿をした時はもう一度`channelKey`を作り、閲覧者にその鍵を新しく教えないといけない。いちいちこれをやるのは不便だ。

## 実装のイメージ
　さてこの問題を解決するための、細かい実装について話す前にイメージを掴んでみよう。
### 次のチャンネル鍵 - nextChannelKey
　MAMでは`message`を暗号化する前に`message`に**`nextChannelKey`（次のチャンネル鍵）**という値を含ませる。RPG風に例えるなら、最初の鍵で開けた宝箱の中に、次の宝箱を開ける鍵を入れるようなものだ。これを繰り返すことで、最初に作った`channelKey`を知っている人は`message`の復号によって得られる`nextChennelKey`を使って、投稿されたMAMを連鎖的に追っていくことができる。また、途中の宝箱を開ける`nextChennelKey`を所有している人は、その鍵を使って途中からチャンネル閲覧を始めることができる。`nextChannelKey`はこれも任意のトライトで問題ない。

![mam_nextKey_1.png](https://qiita-image-store.s3.amazonaws.com/0/187795/035bba8e-d285-3a61-265d-f3fcf9e1b5fc.png)


### メッセージの保管アドレス - messageID
　しかし、今のままだと鍵はあっても宝箱の地図がない。MAM語にすると、`chennelKey`もしくは`nextChennelKey`を持っていても、暗号化された`message`が保管されている**`address`**が分からない。
　MAMでは`channelKey`もしくは`nextChennelKey`が開けられる宝箱の場所情報（`address`）は単純に鍵を二回ハッシュ関数に通して生成\*される。つまり、鍵自体に地図が書いてあると捉えられる。このMAM用に生成されたアドレスのことを**`messageID`**と呼ぶ。

![mam_messageID1.png](https://qiita-image-store.s3.amazonaws.com/0/187795/24322eb3-93d4-b82e-2afd-4d9fd58ae6eb.png)

\* messageIDの生成方法は、チャンネル利用者の間で統一すれば自由に設定できる。ただ、安全性を考えるとハッシュに通したほうがいい。

### メッセージチェーン
　最初に生成した`ChannelKey`が最初の`message`と`nextChennelKey`を暗号化し`messageID`宛てに空送金という形でBundleを生成し、Tangleにアタッチする。それを繰り返して暗号化された`message`の鎖を**メッセージチェーン**と呼ぶ。途中の鍵を渡された人は、メッセージチェーンに途中から参加することができるが、過去の投稿に遡ることはできない。

## 実装の実際
　さて、今までは絵を使って説明してきたが、ここで実際のMAMの話をしよう。
　まず、メッセージチェーンを過去から最新の投稿へ辿る際にいちいち`message`を鍵で復号するのは計算コストが高い。もし、100個投稿したチャンネルの最新記事まで最初から辿っていくとなると膨大な計算量が必要になる。そのため実装では`nextChennelKey`は、任意に決めて`message`に含ませるのではなく、`nextChannelKey = hash(channelKey + salt)`という式で生成できるようにしている。`salt`というのは投稿する時にTransactionオブジェクトの`tag`に入れる値である。
　その`tag`の値を知るには`messageID`が必要だ。`channelKey`からしか`messageID`を見つけられないので、結果的に`channelKey`を知る人しか`nextChannelKey`を知ることができないという機能を保持したまま、最新の投稿に辿り着くコストを低く抑えられる。

　宝箱の例えで言うなら「次の宝箱を開けるnext鍵を宝箱の中に入れるのではなく、宝箱の裏にでも貼り付けておくようなものだ。しかも、たまたま宝箱の前を通りかかった人にはそのnext鍵は見えない。見えるのはその宝箱を開ける鍵を持ってきた人だけ。」という感じだろうか。

![mam_next_key_tx.png](https://qiita-image-store.s3.amazonaws.com/0/187795/af4df8f3-9a12-e897-4d47-a247be596586.png)

　また、`message`が`sigF`の限界2187トライトより長くなったとしても投稿を二回に分ける必要はない。[Bundleの全容](https://qiita.com/ABmushi/items/0c9f73e08fdb6597ab9c#bundle%E3%81%AE%E6%A7%8B%E9%80%A0)でも軽く触れたが、`message`が長くなった分、Bundle内のTransactionを増やせば、どんな長さのトライトも一度に一つのBundleにまとめて投稿できる。ただ、容量の大きなBundleはTangleに貼り付けるためのPoWがその分大きくなりコスパはよくないうえ読み込むのにも時間がかかるが。

# MAMの裏側 - 投稿
　さて、今までざっくり説明した中で語られなかったチャンネルの所有権（投稿権）についての話をしたい。なぜそんな話をするかは、次のようなケースを考えると分かるかもしれない。

　チャンネルに初投稿したAさんはBさんにチャンネルを見て欲しいと考えた。そこで、AさんはBさんにチャンネル鍵を教えた。BさんはAさんにもらった`channelKey`で`messageID`を訪れ、`message`を復号しAさんの投稿を閲覧した。続きが気になったBさんは復号の際手に入った`nextChannelKey`で次の`messageID`（=アドレス）を生成し、次の`message`を見ることにした。しかし、Aさんはまだ次の投稿をしていなかったので、その`messageID`宛てにはまだ何のトランザクションも発行されていなかった。
　BさんはAさんに嫌がらせをしたいと突然思いついた。見渡すとBさんの手には、`nextChannelKey`と次の`messageID`があった。これがあれば、Bさんは次の`message`をBさんが勝手に決めて、`nextChannelKey`で暗号化してこの`messageID`宛てにAさんより先に投稿すれば、Aさんのチャンネルを乗っ取れると考えた。
　これは上手くいくだろうか？上記MAMの表側で説明した原理を元にすれば上手くいくように思える。
...しかし、それではMAMは失敗だ。もちろんこのようなことが起こらないためにMAMは設計されている。この章では、そんなチャンネルの所有権をどう確保するかという話をする。

## チャンネルの所有権問題
　さて、上の問題点を簡潔に述べると**Chaneel Keyの実装だけでは、AさんとBさんどちらがチャンネルの所有者か分からない**ということだ。
　ここでIOTAにおける、アドレスの残高の所有権はどう証明したかを思い出してみよう。アドレスの残高を引き出す際には、Seedから生成される**Private Key**で[署名](https://qiita.com/ABmushi/items/422d1bf94be0c919583a#%E7%BD%B2%E5%90%8D%E3%81%AE%E6%96%B9%E6%B3%95)したトランザクションが承認されることで残高を引き出すことができた。
　MAMではPrivate KeyをMerkle Treeと組み合わせることでチャンネルの所有権を証明するのに利用する。

## Merkle tree based signature scheme 
　MAMにおける**Merkle Tree（マークル木）**を使った独特な署名方法について説明をしたい。[Merkle tree based signature scheme](https://www.imperialviolet.org/2013/07/18/hashsig.html)と言う技術らしいので興味ある人はリンク先を読んで見ると良い。
　また、Merkle Treeというコンピューターサイエンスの専門用語についての解説は省略させていただく。というのも、Merkle Treeは暗号通貨界御用達の技術であり、ビットコイン価格の高騰とともに解説記事も爆発的に増えたため、わざわざここで説明し直す必要がないと判断したからだ。

### Merkle Treeの生成
[ソースコード](https://github.com/iotaledger/mam.client.js/blob/master/lib/merkle.js#L54)
　MAMのMerkle TreeはSeedから生成する。（種が木へ！）Merkle Treeは`start`と`size`という引数をとる。これはSeedから生成されうる`address`の[連鎖](https://iotafan.jp/developer/iota_universe_abmushi_20171213/)のどの部分をMerkle Treeの葉として使うかに用いられる。SeedからPrivate Keyを生成し、`address`を生成するために、`index`という引数をとったことを覚えているだろうか？（忘れてしまった人のための記事は[こちら](https://qiita.com/ABmushi/items/e271ff05884a7d47658d#%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9)。）下の図のA、B、C、Dはそれぞれ`index`が0~3で生成されるPrivate Keyだ。A'、B'、C'、D'は該当Private Keyから生成される`address`である。
![mam_merkle_1-2.png](https://qiita-image-store.s3.amazonaws.com/0/187795/06ea21b7-6427-90b4-1c82-4a64c53a0df1.png)
　Merkle Treeの葉A"、B"、C"、D"には`address`にハッシュ関数を通したものを用いる。葉から`root`へ枝が根に集まるようにハッシュ関数に通していく。図で言うと下のノードから葉の方向へ逆生成させることはできない。

### Siblingsの取得
　Siblings（兄弟）という概念について説明する。
　まず、上のMerkle Tree上の葉`A'`が与えられたとする。`root`を得るためには全ての葉`B'C'D'`が必要になるが全ての葉を知れない場合どうやって`root`を導き出せるか。Siblingsとは葉`A'`とともに`root`を得るために使われるMerkle Tree上の枝のことである。図を見る方が早いかも知れない。
![mam_2_siblings_2.png](https://qiita-image-store.s3.amazonaws.com/0/187795/c3f7d1b4-984b-d4a1-d054-e788fe2a7a10.png)

　今回の例では葉`A'`が与えられた。その場合は`B"`と`Hash(C"D")`があれば**全ての葉を知らなくとも`root`を求めることができる**。このような関係を持つ枝、`B"`と`Hash(C"D")`を`A'`の**Siblings**と呼ぶ。

### 秘密鍵と公開鍵
　署名主が隠したい秘密鍵は今回の場合、Private KeyのA、B、C、Dのペアだ。Seed所有者だけが秘密鍵を持っている。（Private KeyはSeedと同様他人に教えてはダメだ。）そして、署名の公開鍵はA、B、C、Dから生成される`root`と`siblings`である。
　`siblings`から`root`を生成できるのはMerkle Treeを生成した本人だけである。本人以外は`siblings`だけでは足りず、欠けた部分を補う葉が必要だ。
　上の例で考えるなら`index=0`の`siblings=[B",Hash(C"D")]`を与えられた場合、`A'`を持っていないと`root`を生成できない。`A'`は本人しか持っていない。つまり、公開されている情報は`siblings`だけなのに`root`を生成できることが本人であることの証明になる。*※重要なのは`root`を知ることではなく生成できることだ。*
　![mam_2_merkle_pubkey.png](https://qiita-image-store.s3.amazonaws.com/0/187795/42e5b069-c3bf-333e-2d9f-84b7fa916bcb.png)
　
　この仕組みを使ってMAMではチャンネルの本人識別を実現した。さて、次章でついにその本題に入ろう。

# MAMの裏側 - 署名・承認
　ここまで記事で出てきた大きな概念が二つあった。
>1. nextChennelKeyで繋がるメッセージチェーン
>2. Merkle Tree

　この二つを組み合わせてMAMの投稿は成し遂げられる。この章ではついにMAMの実際行われているメッセージ生成の手順を説明していく。
## MAMメッセージの生成 - MAM.create
[ソースコード](https://github.com/iotaledger/mam.client.js/blob/master/lib/mam.js#L63)
　まず、Aさんが初めてチャンネルを開設する際、Aさんは
>1. `channelKey`を一つ生成。
2. 同じ`size`のMerkle Treeを`start`から２つ分生成。

　Merkle Tree２つだが、どちらとも*Merkle Treeの生成*で説明した方法で作成する。１つ目`tree0`は`start0 = start`、`size0 = size`。２つ目`tree1`は`start1 = start0+size0`、`size1 = size0`。言い換えると生成されるPrivate Keyの連鎖で１つ目のMerkle Treeが使っていない次の部分を使う。下図参考。
![mam_2_double_merkle.png](https://qiita-image-store.s3.amazonaws.com/0/187795/67d5fc56-b28f-4d91-65c5-9a56b416d240.png)
　MAM投稿の時、こうして生成された２つのMerkle Treeのうち`tree0`の木丸ごとと`tree1`の`root`（**nextRoot**）を引数にとる。また、**葉番号**という値を**0以上size未満**から選ぶ。今回は分かりやすく`leaf_index = 0`としよう。**葉番号**はMerkle Treeの葉の一番左から何番目を示す。`tree0`の葉番号0は`A'`、`tree1`の葉番号2は`G'`である。

```java:MAM.createの例
leaf_index = 0    // 葉番号

const mam = new MAM.create({
    message: iota.utils.toTrytes(message),  // messageをトライトに変換
    merkleTree: tree0,                      // １つ目のMerkle Tree
    index: leaf_index,                      // 葉番号
    nextRoot: tree1.root.hash.toString(),   // 次のroot。上図のroot_1。
    channelKey: channelKey,                 // ChannelKey（このメッセージの暗号化に使われる。）
});
```
　`MAM.create`の中で行われることを次に説明する。
　まず、`tree0`の**Siblings**を求める。今回与えられる葉は先ほど決めた**葉番号**の葉とする。ということは`leaf_index = 0`なので`siblings`は`B"`と`Hash(C"D")`になる。
![mam_2_small_sib.png](https://qiita-image-store.s3.amazonaws.com/0/187795/d67e16e9-7ad9-d54e-4ba6-978af070fc0d.png)
　次に、`messageTrytes`と呼ばれる**「nextRootと平文を足した文字列」**を署名されるデータとして**葉番号のPrivate Key**で署名を作る。署名作成については[こちら](https://qiita.com/ABmushi/items/422d1bf94be0c919583a#%E7%BD%B2%E5%90%8D%E3%81%AE%E6%96%B9%E6%B3%95)でも説明したが、それを踏まえて下図のように署名は作られる。
![mam_2_sig2.png](https://qiita-image-store.s3.amazonaws.com/0/187795/5c4af53b-d673-6e3b-b71b-ee9778df1335.png)
　こうして今、手元にある値を使ってMAMの１つのメッセージは作られる。それを図示すると下のようになる。
![mam_2_overview_single.png](https://qiita-image-store.s3.amazonaws.com/0/187795/bc220ff5-85ff-8cfe-2fac-0cadf57b32d1.png)
## MAMメッセージ閲覧 - MAM.parse
[ソースコード](https://github.com/iotaledger/mam.client.js/blob/master/lib/mam.js#L131)
　次に投稿されたメッセージを閲覧する方法について説明する。これを読むことで今まで出てきた話がついに一つにまとまる。
### チャンネル鍵と**root**を閲覧者に教える
>**チャンネル鍵**はメッセージの復号のための鍵、`messageID`（アドレス）として閲覧者に教える。そして、メッセージがAさんのものだと照らし合わせるための勘合として**`root`**を閲覧者に渡す。

　この例だと、チャンネル鍵と`tree0`の`root_0`を閲覧者にチャンネル鍵として渡す。ここでBさんが閲覧者としてAさんからチャンネル鍵とrootを教えてもらったとしよう。
　Bさんはチャンネル鍵からメッセージの保管アドレス`messageID`を作ってメッセージを見つける。そして、チャンネル鍵でメッセージを復号する。
　次に、復号したメッセージの署名を`messageTrytes`（署名されるデータ）で承認する。署名の承認の仕方は[こちら](https://qiita.com/ABmushi/items/422d1bf94be0c919583a#%E6%89%BF%E8%AA%8D%E3%81%AE%E6%96%B9%E6%B3%95%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%81%AE%E9%80%86%E7%94%9F%E6%88%90)。

　![mam_2_sig_address.png](https://qiita-image-store.s3.amazonaws.com/0/187795/464abb92-1775-8faa-8870-bf8e86fe2df9.png)
### 本人のメッセージか検証
　次に、承認して得られたアドレスが`leaf_index`の場所のアドレスとして`Siblings`を使ってその`root`を求める。こうして求められた`root`（下図のroot_0）がAさんからもらった`root`と一致すれば、メッセージはAさんのものだと閲覧者は判断できる。
![mam_2_address_merkle.png](https://qiita-image-store.s3.amazonaws.com/0/187795/052d06e5-640a-6c12-5467-df1751d0a1db.png)
　そうでない場合はどういうことか。署名を承認する時に使う`messageTrytes`の内容がAさんが作ったものと違う場合、得られるアドレスが変わる。そのアドレスと`Siblings`を使ってrootを求めると、もちろん得られる`root`の値も変わる。そして、Aさんから教えてもらった`root`と一致しない。
　こうすることで、もし悪意ある者がチャンネル鍵を使って同じ`messageID`（アドレス）宛に全くAさんと関係のないメッセージを投稿したとしても、このrootの検証作業で最終的に弾かれる。

## メッセージチェーンの構築 - nextRoot
　MAMはメッセージチェーンだ。一つのメッセージを復号すれば、`nextChannelKey`を使って次のメッセージも閲覧できる。ということは、その次のメッセージがチャンネル所有者本人が投稿したものか検証する必要がある。そのため、メッセージには`nextChannelKey`の他に、`nextRoot`という値も含ませる。この`nextRoot`は`messageTrytes`に平文と一緒に含まれているため署名されるデータの一部である。`nextRoot`生成するたびに、上の図で言う所のMerkle rootの生成に使われる葉（ABCDEF...）が右にどんどんずれていく。（`start`が大きくなっていく。）
　次の投稿を`nextChannelKey`で復号した際には、前項で説明したように今度は`nextRoot`と最終的に得られる`root`と一致するかを確認する。

## 小休止
　理解できただろうか？想像以上に多くのアイデアが詰め込まれていたことに驚いたかもしれない。筆者も文でうまく説明できたか不安だ。
　不明点等あれば公式Slackで筆者@abmushi宛にDMでもチャットでも良いので質問をじゃんじゃん投げて欲しい。質疑応答はお互いの理解が深まる絶好のチャンスだ。

# チェーンフォーク - 分裂
　最後にMAMを特徴づける**分裂**という機能についても説明したい。ブロックチェーンのようにメッセージチェーンもフォークする。
　メッセージを分裂させたいときは、単純に葉番号`leaf_index`が違う`siblings`を含むメッセージを投稿すれば良い。こうすることで同じ`messageID`（アドレス）に本人検証も問題なくできるメッセージを複数（最大はMerkle Treeの`size`）持てる。
　また、`nextChannelKey`の生成方法も（nextChannelKey=hash(channelKey,leaf_index)）というように`leaf_index`に依存するようにすれば、フォーク後全く違うアドレスを辿るようにチェーンを伸びていかせることもできる。

## 利用例
　筆者が思いついたこのチェーンフォークの用途は、MAMのメッセージチェーン自体をディレクトリのツリー構造として利用すること。
　まず最初にルートディレクトリを投稿する。そのディレクトリの子ディレクトリの数だけ分裂させることを繰り返せば、Tangle上にツリー構造を作れる。また、どの部分のチャンネル鍵を教えるかによってファイルのアクセス権限も持たせることができる。

# MAMとはプロトコル
　MAMとはそれ自体が発行者が自由に決められるプロトコルである。投稿者と潜在的な閲覧者の間でMAMの各種値（`nextChannelKey`、`messageID`、や`nextRoom`）の計算方法を統一することで、この記事で紹介した方法以外の手順を使ってMAMを発行できる。

# 最後に
　MAMを理解したいという気持ちはずっと持っていたものの、今IOTAが取り組んでいる課題は別のところにあり、コミュニティで具体的にはほとんど語られず、ビジョンとしてのみ存在していたこのMAM。結局公式のソースコードを読んで自分で理解するしか手段がなかった。
　その結果、IOTAのBundleや署名などの根幹技術がコードレベルでどうなっているか理解できたので結果的にはものすごくためになった。
　記事中でも今まで投稿したIOTAの記事の知識が前提になることが多く数え切れないほど引用リンクを貼った。間違いなくこの記事は今年の集大成だろう。
　それではみなさん良いお年を！

# 参考文献
JSのコード：[mam.client.js](https://github.com/iotaledger/mam.client.js)
公式アナウンス：[Introducing Masked Authenticated Messaging](https://blog.iota.org/introducing-masked-authenticated-messaging-e55c1822d50e)
外観：[Overview](https://github.com/iotaledger/mam.client.js/blob/master/Overview.md)
たまたま見つけた中国語の記事：[MAM　筆記](https://hackmd.io/c/rkpoORY4W/%2Fs%2FrJkpIrrbM)
