IOTA:Signature And Validation

# Curl and Kerl
　link [here](https://github.com/iotaledger/kerl)。

# Address generation
 First of all, create **Private Key** from **Seed**.
 
 ```javascript:
// length = security (1: light client, 2: wallet default, 3: exchange level)
var key = function(seed, index, length) {
...
    return key;    // private key
}
 ```
> 1. have your Private Key ready.
> 2. divides the Private Key into 'L' segments, where `L = security * 27`.
> 3. Hash all segments as a whole. The product is called `digest`.
> 4. Hash `digest` twice. The product is called `address`.

![address_gen2.png](https://github.com/abmushi/iota/blob/master/qiita/docs/sig/address_gen2.png)

# Signature
Signature is used to sign anything(=signed data usually bundle) on tangle that belongs to you with your private key.

> 1. have your Private Key ready.
> 2. divides the Private Key into 'L' segments, where `L = security * 27`.
> 3. For each *i*-th segment, hash N_*i* times, where N_*i* is caluculated as followed:
> > **How to get N**
> >
> > For each *i*-th tryte of the **Signed Data**, get decimal 'd' of the tryte. Converter [here](https://github.com/abmushi/iota/blob/master/qiita/docs/Signature-en.md#tritstryte-to-decimal-table). e.g) tryte[9] corresponds to `d=0`, [A] is to `d=1`...[M] is to `d=13`, L is to `d=-13`...Y is to `d=-2`, Z is to `d=-1`).
> >
> > Formula: *N_i = 13 - d*
> 4. Those hashed segments are called **Signature** together.

![signing1.png](https://github.com/abmushi/iota/blob/master/qiita/docs/sig/sig.png)

# Validation (address Re-generation )
> 1. have your Signature ready.
> 2. divides the Signature into 'L' segments, where `L = security * 27`.
> 3. For each *i*-th segment, hash M_*i* times, where M_*i* is caluculated as followed:
> > **How to get M** (basically main idea is same as N.)
> >
> > For each *i*-th tryte of the **Signed Data**, get decimal 'd' of the tryte. Converter [here](https://github.com/abmushi/iota/blob/master/qiita/docs/Signature-en.md#tritstryte-to-decimal-table). e.g) tryte[9] corresponds to `d=0`, [A] is to `d=1`...[M] is to `d=13`, L is to `d=-13`...Y is to `d=-2`, Z is to `d=-1`).
> >
> > Formula: *M_i = 13 + d*
> 4. Hash those segment together and get `digest`.
> 5. Hash the `digest` twice.
> 6. Check if the product of step 5 matches the address of the signed data(usually Bundle).

![validate1.png](https://github.com/abmushi/iota/blob/master/qiita/docs/sig/val.png)

# Signed Data
　Signature is used to sign your input address when you spend. And signature is stored in the bundle that spends the signed input. Signature data (length = security * 2187 tryte) is stored at `signatureFragment`. (Note that `signatureFragment`'s capacity is 2187 tryte, so the larger security, the more transactions for storing signature are necessary to be included in the bundle.)
 Signed data mentioned above refers to the bundle hash (81 tryte) that includes the signature.
 （Strictly speaking, signed data is called normalized bundle hash, which is slightly incremented bundle hash.）

 ![singed_data.png](https://github.com/abmushi/iota/blob/master/qiita/docs/sig/norm.png)

　data[0], data[1], data[2], which are components of normailized bundle hash, are used as *Signed Data*. How many times to hash each of 27 segments coressponds to each tryte of 27 trytes signed data. data[i] above is 27 trytes of signed data. if `security = 1`, data[0] is used. if `security = 2`, data[0] and data[1] is used such that in total, 54 trytes are used to sign. (table above)
 Recall the when creating bundle, numbers of transactions that store signature depends also on the security level. That was because as security level increases, more data[i] is used to sign.
 If `security >= 4`, signature is created with data loop: data[3] does not exist so use data[0] again.

## Normalized Bundle
```java:Bundle.java
/**
     * Normalized the bundle.
     * return the bundle each tryte is written in integer[-13~13]
     *
     * @param bundleHash BundleのHash。
     * @return normalizedBundle A normalized bundle hash.
     */
    public int[] normalizedBundle(String bundleHash) {

        //  normalized Bundle 81 trytes.
        int[] normalizedBundle = new int[81];

        //  divides bundle hash into three sections, 27 trytes each.
        for (int i = 0; i < 3; i++) {
        
            long sum = 0;

            //  check each tryte in a section.
            //  get corresponding integer [-13~13]. And add it to sum.
            for (int j = 0; j < 27; j++) {

                //  sum += value, where
                //  value = integer value of i*27+j-th tryte
                sum += 
                    (normalizedBundle[i * 27 + j] = 

                        //  Convert tryte[9ABC...Z] into [-13~13]
                        Converter.value(Converter.tritsString("" + bundleHash.charAt(i * 27 + j)))
                    );
            }

            // if sum of the section >= 0
            if (sum >= 0) {

                //  until sum = 0
                while (sum-- > 0) {

                    //  decrement tryte
                    for (int j = 0; j < 27; j++) {
                        if (normalizedBundle[i * 27 + j] > -13) {
                            normalizedBundle[i * 27 + j]--;
                            break;
                        }
                    }
                }

            //  if sum of the section < 0
            } else {

                //  until sum = 0
                while (sum++ < 0) {

                    //    increment tryte
                    for (int j = 0; j < 27; j++) {

                        if (normalizedBundle[i * 27 + j] < 13) {
                            normalizedBundle[i * 27 + j]++;
                            break;
                        }
                    }
                }
            }
        }

        return normalizedBundle;
    }
```

# Risk of Address Reuse
 You must have seen the warnings "Do not reuse the address!". But, what's that? And why can't we just simply use same address?
 Secret is here. Recall:
> **How to get N**
> 
> For each *i*-th tryte of the **Signed Data**, get decimal 'd' of the tryte. Converter [here](https://github.com/abmushi/iota/blob/master/qiita/docs/Signature-en.md#tritstryte-to-decimal-table). e.g) tryte[9] corresponds to `d=0`, [A] is to `d=1`...[M] is to `d=13`, L is to `d=-13`...Y is to `d=-2`, Z is to `d=-1`).
>
> Formula: *N_i = 13 - d*

 Number of hashings depends on i-th tryte of signed data. If signed data contains a lot of 'M', which requires zero hashing. This may result in the exposure of the part of your raw private key. 

## Quantum Secure
 This kind of signing mechanism originates from [Winternitz one-time signature](https://eprint.iacr.org/2011/191.pdf).

# Trits/Tryte to Decimal Table
<img width="184" alt="tryte.png" src="https://qiita-image-store.s3.amazonaws.com/0/187795/e325fe61-7773-8e64-46e0-2e98d66aacf4.png">

# Reference
IOTA iotaledger [https://github.com/iotaledger](https://github.com/iotaledger)

signing part:
JavaScript=>[signing.js](https://github.com/iotaledger/iota.lib.js/blob/master/lib/crypto/signing/signing.js).

Java=>[Signing.java](https://github.com/iotaledger/iota.lib.java/blob/master/jota/src/main/java/jota/utils/Signing.java).

# About Author
@abmushi on [twitter](https://twitter.com/abmushi), discord

Translated from my original article written in Japanese [here](https://qiita.com/ABmushi/items/ab523d838bf71ca385d4)

Donation is always welcome and appreciated!

BTC: `1ACGpgpAMgaAKbGpPq2sDa467MnRNdW4wX`

IOTA: `KWIEEQHAJBJTDPE9WEDILKMVQCJPZSF9CXALYQTULCGNPLIIKJLFYHCWSJNXDALKHAOOTELQUIXWIOFVDPQNXMLBZB`
