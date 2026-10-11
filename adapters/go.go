package main
import("bufio";"crypto/sha256";"encoding/hex";"encoding/json";"fmt";"io";"os";"path/filepath";"sort";"strconv";"strings")
type Entry struct{Rel string;Dir bool}
func must(e error){if e!=nil{panic(e)}}
func walk(root string)[]Entry{out:=[]Entry{};must(filepath.WalkDir(root,func(p string,d os.DirEntry,e error)error{if e!=nil{return e};if p!=root{r,e:=filepath.Rel(root,p);if e!=nil{return e};out=append(out,Entry{filepath.ToSlash(r),d.IsDir()})};return nil}));return out}
func read(p string)[]byte{b,e:=os.ReadFile(p);must(e);return b}
func sum(b []byte)int64{var h int64;for _,x:=range b{h=(h*31+int64(x))%1000000007};return h}
func exists(p string)bool{_,e:=os.Stat(p);return e==nil}
func cp(p,q string){a,e:=os.Open(p);must(e);defer a.Close();b,e:=os.Create(q);must(e);_,e=io.Copy(b,a);must(e);must(b.Close())}
func execute(kind,root,dest string,n,variant int)[][]any{rows:=[][]any{};lines:=[]string{};entries:=walk(root)
if kind=="relocate"{must(os.MkdirAll(dest+"/moved",0755));ents,e:=os.ReadDir(dest);must(e);for _,x:=range ents{if x.Name()!="moved"{must(os.Rename(dest+"/"+x.Name(),dest+"/moved/"+x.Name()))}}}
for _,entry:=range entries{rel:=entry.Rel;p:=root+"/"+rel;q:=dest+"/"+rel;if entry.Dir{if kind=="walk"{rows=append(rows,[]any{rel,-1,0})};continue};if kind=="walk"{rows=append(rows,[]any{rel,0,0});continue};if kind=="mixed"&&(strings.HasPrefix(rel,"group19/")||(!strings.HasSuffix(rel,".md")&&!strings.HasSuffix(rel,".dat"))){continue};st,e:=os.Stat(p);must(e);size:=st.Size();var v any=int64(0)
if kind=="filter"{id,e:=strconv.Atoi(filepath.Base(rel)[1:7]);must(e);if id%100>=variant{continue}}
if kind=="read"||kind=="hash-portable"||kind=="mirror"||kind=="detect-hash"||kind=="clean"||kind=="manifest"||kind=="generate"||kind=="mixed"{v=sum(read(p))}
if kind=="large-read"{b:=read(p);v=int64(b[0])*256+int64(b[len(b)-1])}
if kind=="hash-sha256"{h:=sha256.Sum256(read(p));v=hex.EncodeToString(h[:])}
if kind=="detect-mtime"&&exists(q){s,e:=os.Stat(q);must(e);if st.ModTime().Unix()==s.ModTime().Unix(){continue}}
if kind=="detect-hash"&&exists(q)&&v==sum(read(q)){continue}
if kind=="clean"{if !exists(q){rows=append(rows,[]any{rel,"missing",0})}else if v!=sum(read(q)){rows=append(rows,[]any{rel,"modified",0})};continue}
if kind=="mixed"&&!strings.HasSuffix(rel,".md")&&!strings.HasSuffix(rel,".dat"){continue}
if kind=="large-write"||kind=="write"||kind=="overwrite"||kind=="copy"||kind=="mirror"||kind=="generate"||kind=="mixed"{must(os.MkdirAll(filepath.Dir(q),0755));if kind=="mixed"&&strings.HasSuffix(rel,".dat"){cp(p,q)}else if kind=="generate"||kind=="mixed"{must(os.WriteFile(q+".generated",append([]byte("generated\n"),read(p)...),0644))}else if kind=="mirror"{if !exists(q)||v!=sum(read(q)){cp(p,q)}}else if kind=="copy"{cp(p,q)}else{must(os.WriteFile(q,read(p),0644))}}
if kind=="rename"{must(os.Rename(q,q+".renamed"))};if kind=="delete"{must(os.Remove(q))};if kind=="manifest"||kind=="generate"||kind=="mixed"{lines=append(lines,fmt.Sprintf("%s\t%d\t%v\n",rel,size,v))};rows=append(rows,[]any{rel,size,v})}
if kind=="mirror"||kind=="clean"{for _,ent:=range walk(dest){if !ent.Dir&&!exists(root+"/"+ent.Rel){if kind=="mirror"{must(os.Remove(dest+"/"+ent.Rel))}else{rows=append(rows,[]any{ent.Rel,"unexpected",0})}}}}
if kind=="manifest"||kind=="generate"||kind=="mixed"{sort.Strings(lines);must(os.WriteFile(dest+"/manifest.tsv",[]byte(strings.Join(lines,"")),0644))};return rows}
func main(){fmt.Println("BOOT");s:=bufio.NewScanner(os.Stdin);for s.Scan(){p:=strings.Split(s.Text(),"|");n,e:=strconv.Atoi(p[3]);must(e);v,e:=strconv.Atoi(p[4]);must(e);b,e:=json.Marshal(execute(p[0],p[1],p[2],n,v));must(e);fmt.Println(string(b))};must(s.Err())}
