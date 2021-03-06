## STEP Week6

### 宿題1<br>
```
def foo(b):
   b.append(2)
   b = b + [3]
   b.append(4)
   print('b:', b)
a = [1]
foo(a)
print('a:', a)
```
を実行すると出力は
```
b: [1, 2, 3, 4]
a: [1, 2]
```
となる。<br>

この関数について、idを使って各変数が指しているアドレスをprintしたうえで、メモリ上でのどのようにデータが保管されているかを説明する。<br>
それを踏まえた上で、なぜ関数内で実行したappendが関数の外で定義した変数に影響を及ぼしてしまうのかを説明する。<br>


a,bだけでなく、その配列の中身のidもprintした。
```
python3 ./homework1.py
```
とすると出力は<br>
```
id(a): 0x10303a1e0
id(b): 0x10303a1e0
id(b[0]): 0x102f37f20
id(b[0]): 0x102f37f20
id(b[1]): 0x102f37f40
id(b): 0x10303a1e0
id(b): 0x103281d70
id(b[0]): 0x102f37f20
id(b[1]): 0x102f37f40
id(b[2]): 0x102f37f60
id(b): 0x103281d70
id(b[0]): 0x102f37f20
id(b[1]): 0x102f37f40
id(b[2]): 0x102f37f60
id(b[3]): 0x102f37f80
b :  [1, 2, 3, 4]
id(a): 0x10303a1e0
a :  [1, 2]
```
となった。この結果から以下のようなことが考えられる。なお、図はメモリを簡略化したものであり、ポインタの番号も説明のために適当に割り振っている。<br>

1. まず、a = [1]とすると、[1]を参照するポインタ*1e0がaに割り当てられる。<br>
2. fooの中身を見ていく。def foo(b)のbとしてaを代入したのでこのbはaと同じポインタ(*1e0)を持つ。<br>
3. b(*1e0).append(2)、*1e0 = [1,2]
4. b = b + [3]。この時、左辺のbには新しいポインタ(*d70)が割り当てられる。*d70 = *1e0 + [3] = [1,2,3]なので左辺のbの値は[1,2,3]になる。<br>
5. b(*d70).append(4)、*d70 = [1,2,3,4]<br>
6. print(b)のbは\*d70というポインタを持ち、その値である[1,2,3,4]がprintされる。<br>また、print(a)のaのポインタは*1e0なので、その値である[1,2]がprintされる。<br>

＊fooを抜けるとfooの中で使われたメモリはfreeされる。byメンターさん<br>

以上の理由より、aは関数内の計算の影響を受ける。また、それがbと異なった値になる。<br>

<img width="700" src="./images/1.jpeg"><br>
<img width="700" src="./images/2.jpeg"><br>
<img width="700" src="./images/3.jpeg"><br>
<img height="270" src="./images/4.jpeg"><br>


### 宿題２<br>
mmapとmunmapを使って最強の malloc / free を作ってみよう！！ <br>
最強に効率がよいメモリ管理のアルゴリズムを考えよう<br>

効率がよいとは？<br>
1. 速い
2. 使用率（実際に使っている領域/mmapした領域）が高い


**＜方法１＞**<br>
free_listの頭に新しくリストが追加される度に、その隣のmetadata(アドレスcur_metadata+1+size)がfree_listに含まれているかを調べ、含まれていれば合体させる。<br>
```
gcc malloc_unite_free.c -lm
./a.out
```
結果
```
Challenge 1: simple malloc => my malloc
Time: 24 ms => 1720 ms
Utilization: 70% => 70%
==================================
Challenge 2: simple malloc => my malloc
Time: 18 ms => 979 ms
Utilization: 40% => 40%
==================================
Challenge 3: simple malloc => my malloc
Time: 290 ms => 14276 ms
Utilization: 8% => 17%
==================================
Challenge 4: simple malloc => my malloc
Time: 30473 ms => 88432 ms
Utilization: 15% => 29%
==================================
Challenge 5: simple malloc => my malloc
Time: 29100 ms => 105938 ms
Utilization: 15% => 24%
==================================

```
時間はかなりかかってしまうが、使用率が上がっていることがわかる。<br>


**＜方法２＞**<br>
さらに使用率を上げるため、munmap_to_system()で不要になったsize4096の領域をシステムに返すことにした。具体的には、一番最後にmmapしてきた領域のメタデータを覚えておき、free_listにそのメタデータが含まれる、かつ大きさが4096以上ならmunmapするようにした。
```
gcc malloc_unite_free_munmap.c -lm
./a.out
```
結果
```
Challenge 1: simple malloc => my malloc
Time: 21 ms => 3233 ms
Utilization: 70% => 70%
==================================
Challenge 2: simple malloc => my malloc
Time: 21 ms => 1754 ms
Utilization: 40% => 40%
==================================
Challenge 3: simple malloc => my malloc
Time: 549 ms => 26620 ms
Utilization: 8% => 17%
==================================
Challenge 4: simple malloc => my malloc
Time: 33187 ms => 122082 ms
Utilization: 15% => 29%
==================================
Challenge 5: simple malloc => my malloc
Time: 29120 ms => 162697 ms
Utilization: 15% => 24%
==================================
```
残念ながら時間だけ増えて使用率は変わらなかった。全てのmmap領域を記憶するようにすればもう少し使用率が上がりそう。実装しようとしたがリストをもう一つ作ったら混乱して挫折した。<br>


**＜方法３＞**<br>
Best-fitと空白連結の方法（方法１）を組み合わせた。Best-fitでは、フィットするものがなかった時、一番大きさが近いものを取ってくるようなプログラムにしようとしたらうまくいかなかった（多分凡ミス）ので、フィットするものがなかったらFirst-fitに切り替えるようにした。結果的にこれが時間短縮に繋がった気がする。<br>
また、空白連結の際に、free_headの方に連結するような仕組みにしたため、first-fitをする際に空いている領域をすぐに見つける確率が高くなっており、それも高速になった理由の一つかもしれない。<br>
```
gcc malloc_unite_free_best_fit.c -lm
./a.out
```
<img height="450" src="./images/5.jpeg"><br>
結果
```
Challenge 1: simple malloc => my malloc
Time: 21 ms => 1237 ms
Utilization: 70% => 70%
==================================
Challenge 2: simple malloc => my malloc
Time: 19 ms => 692 ms
Utilization: 40% => 40%
==================================
Challenge 3: simple malloc => my malloc
Time: 276 ms => 832 ms
Utilization: 8% => 50%
==================================
Challenge 4: simple malloc => my malloc
Time: 32967 ms => 2777 ms
Utilization: 15% => 76%
==================================
Challenge 5: simple malloc => my malloc
Time: 24778 ms => 1851 ms
Utilization: 15% => 78%
==================================
```
これが一番良い結果となった。<br>


#### ＊メンターさんから問題<br>
Q.同時にheapが呼ばれると衝突してcollapseするため、普通、heapを使っているときはlockをかけて他からアクセスできないようにする。これでcollapseは防げるが問題がある。何でしょう？<br>

A.lockが外れるまでheapが使えないため、heapの順番待ちになって、処理が遅くなってしまう。<br>
解決策は色々あるし、今も考えられ続けているらしい。<br>
今回でいうと、mallocを頻繁に呼ぶことがこれに当たる。一つの解決策として、このmalloc専用のheapを作るということが挙げられる。ただし、このheap専用のメモリを確保しておくことになるのでメモリの消費量は増えてしまう。<br>



