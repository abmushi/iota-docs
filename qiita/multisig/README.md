
# address.js
[ソース](https://github.com/abmushi/iota/blob/master/qiita/multisig/address.js)
　Seedを複数用意してマルチシグアドレスを生成する。
 
>SeedやSecurityの値は保存されないので安全だが、その分自己責任でSeedは保管する必要がある。

## 使い方
iota.lib.jsをダウンロードし、その中の/example/のディレクトリ内にこのコードを保管し、`node address.js`で実行すればOK。

なお、`npm install readline-sync`で必要パッケージ`readline-sync`をインストールしておく必要がある。[詳細](https://www.npmjs.com/package/readline-sync/tutorial)

```shell
いくつのSeedを使用しますか? ( 1 以上): 3
Seed[1/3]: #################################################################################
Reinput a same one to confirm it: #################################################################################
Security(1~3): 2
- 注意 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
 - Seedは必ずオフラインで保管しましょう。Seedを失くすと資産を消失します。
 - Securityの値も忘れないようにしましょう。
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Seed[2/3]: #################################################################################
Reinput a same one to confirm it: #################################################################################
Security(1~3): 3
- 注意 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
 - Seedは必ずオフラインで保管しましょう。Seedを失くすと資産を消失します。
 - Securityの値も忘れないようにしましょう。
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Seed[3/3]: #################################################################################
Reinput a same one to confirm it: #################################################################################
Security(1~3): 3
- 注意 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
 - Seedは必ずオフラインで保管しましょう。Seedを失くすと資産を消失します。
 - Securityの値も忘れないようにしましょう。
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
- 注意：２個以上のSeedをどの順番で入力したかも忘れないでください。
current index: 0
- - - - - - - - - - - - - - - - - - - - 
 - index              :  0
 - address            :  JLCEBALRMRSIZQLTCJEPWZQRTMGBMYCQD9CBUEAKNXHUYLPXV99QLMNLGU9GSCUDAZ9FIRXPITCOKXIBX
 - address + checksum :  JLCEBALRMRSIZQLTCJEPWZQRTMGBMYCQD9CBUEAKNXHUYLPXV99QLMNLGU9GSCUDAZ9FIRXPITCOKXIBXKRKBQGUFD
- - - - - - - - - - - - - - - - - - - - 
Want next index? [y/n]: y
- - - - - - - - - - - - - - - - - - - - 
 - index              :  1
 - address            :  OFANKQYTQYPUQPJPEDUSOFGKTWS9SWDWMXEWTKHAVGRYVCHCXN9WVUKKNWUSNLIBZHYRFHSWJWZNHOZMC
 - address + checksum :  OFANKQYTQYPUQPJPEDUSOFGKTWS9SWDWMXEWTKHAVGRYVCHCXN9WVUKKNWUSNLIBZHYRFHSWJWZNHOZMCXUYN9FWAX
- - - - - - - - - - - - - - - - - - - - 
Want next index? [y/n]: n
```
