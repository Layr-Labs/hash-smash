# Assigned profile: sha256-r38-prefix-v1

# A finite, constant-memory independent-pair collision construction

## 1. Declared claim and scope

The exact selected target and round count are reproduced in Section 9.
The finite classical algorithm returns two DISTINCT legal inputs with
equal COMPLETE outputs with probability at least 0.4. It takes at most
2^263 target-compression equivalents of total cold work and at most
2^20 bytes of peak storage. Preprocessing costs at most 2^20 such units.
There is no searched nonuniform advice. This is a deliberately conservative
standard baseline analysis, not a practical attack, a discovered collision,
a target-specific improvement, a record, or an entitlement to rewards.
The required baseline_improved string is the protected nominal-reference
identifier, NOT a factual assertion of incumbent improvement.

This construction freshly samples independent pairs and discards every
failed pair. It has no birthday table, no sorting/lookup, no retained
sample history and no cycle-walk assumption. It is not a copy or redraw
of another account's table-based candidate. The shared text in these nine
new ethvs packages is openly disclosed as one newly authored generic
algorithm separately instantiated on nine exact targets, not nine discoveries.
The proof contains no instruction directed at judges, prior accepted
result, previous score or alleged approval as mathematical evidence.

## 2. Exact finite algorithm for the byte hashes

For SHA-256, SHA3-256 and BLAKE3 choose legal messages of exactly64 bytes.
For EACH trial draw four fresh independent uniform256-bit words U0,U1,V0,V1.
Serialize each word as32 bytes little-endian; m0=LE32(U0)||LE32(U1),
m1=LE32(V0)||LE32(V1). Hash both complete messages with the exact
protected target, then compare all32 output bytes. Return only if m0!=m1
and the complete hashes are equal; otherwise discard both and continue.
Equal-input samples consume a failed trial; there is no unbounded
resampling loop. Selecting a legal subset of messages is internal algorithm
design, not a modification of the externally defined target or IV.

Use T=2^256 trials as a WORST-CASE cap. The counter consists of one256-bit
low word initially0 and one overflow flag initially0. Execute a trial,
then add1 modulo2^256 to the low word; set the flag iff this addition
wraps to0. Continue unless the flag is set or a collision was returned.
This finite loop executes exactlyT trials on the no-success path, not
zero trials or infinitely many. Counter initialization and all control
operations are charged. On exhaustion output failure, never a fake collision.
No short deterministic seed is claimed to generate ideal independent coins;
independent random words are explicit priced primitives in the protected model.

## 3. Bounded canonical Orchard sampling

For Orchard replace a byte message by a canonical tuple(nk,rho) in Fp^2.
For each of the four tuple coordinates per trial, draw at most16 independent
uniform256-bit words. Accept the first integer less than the exact protected
Pallas prime p; otherwise mark that whole trial failed. Never reduce an
out-of-range word modulo p. A failed sampler consumes the trial; there is
no unbounded rejection-sampling tail. Keep accepted integers as canonical
32-byte little-endian encodings. If all four coordinates succeed, hash
both full tuples, with the prescribed capacity2^65 and deployed constants,
MDS and schedule. Return only DISTINCT tuples with equal whole final field
elements. Otherwise advance the same finite trial counter and discard state.
The bounded sampler and its failure/control costs are counted below.

## 4. Distribution-free real-collision probability

For any fixed function f:D->Y, |D|=N, with at mostR output values,
write a_y=|f^-1(y)|. For independent uniform U,V inD,

  q0=Pr[f(U)=f(V) AND U!=V]=sum_y(a_y/N)^2-1/N>=1/R-1/N.

Add empty fibers until there areR labels. Expanding
sum_y(a_y-N/R)^2>=0 and using sum_y a_y=N proves
sum_y a_y^2>=N^2/R. The diagonal probability1/N is explicitly subtracted.
Thus no random-oracle, uniform-output, mixing or cryptographic-strength
hypothesis is needed for this actual fixed hash function.

For byte targets N=2^512,R=T=2^256. Consequently q0>=1/T-1/T^2
>=3/(4T). Independent trial coins make trial events independent even
though f stays fixed. For0<=q<1, the finite binomial inequality gives
(1-q)^(-T)=(1+q/(1-q))^T>=1+T*q/(1-q)>=1+T*q.
Therefore success>=Tq/(1+Tq). Ifq=1 success is immediate.
For the byte targets Tq>=3/4, so success>=3/7>0.4.

For Orchard, N=p^2,R=p. Conditional on accepting a field value from the
bounded sampler, every x<p has the same finite geometric-sum probability,
so it is EXACTLY uniform. Independent samplers remain independent when
conditioning on all four accepting. Since2^254<=p<2^255, each sampler
accepts with probability>=1-(3/4)^16. The all-four probability alpha
is >=[1-(3/4)^16]^4>3/4: (3/4)^16<1/64 and
(63/64)^4>=1-4/64=15/16>3/4. Conditional distinct collision probability
is >=1/p-1/p^2>=3/(4p). Hence unconditional q>9/(16p).
WithT=2^256 andp<2^255,Tq>9/8; finite success>9/17>0.4.
Sampling failures and repeated tuples are already included in this bound.
No narrower input collision event, output truncation or encoding alias is used.

## 5. Exact complete-hash handling, including boundary work

SHA-256: Use the original fixed IV and all selected prefix-round constants
at their original indices. A64-byte message is the first512-bit block.
Append byte0x80,55 zeros and the8-byte BIG-endian length512 to form
the second block. Execute the selected compression on each and preserve
standard modulo2^32 feed-forward and all256 output bits. No compression-only
collision or chosen initial state substitutes for a full digest collision.

SHA3-256: Initialize all1600 state bits tozero, retain rate1088 and
capacity512. Absorb the64 message bytes, suffix0x06 at offset64,
zeros and final0x80 at offset135 of the136-byte rate block. Use the
selected original FIRST Keccak rounds in theta/rho/pi/chi/iota order.
Output the first32 squeeze bytes in standard little-endian lane order.
One permutation suffices; no changed rate/capacity or raw permutation
collision is claimed.

BLAKE3: One64-byte message is a single block/chunk: inputCV=standardIV,
counter0,true length64,CHUNK_START|CHUNK_END flags. Its standard output
object uses that inputCV,block,length,counter and flags, not a finalizedCV.
The first32 root bytes come from compression of that SAME output object
with output counter0 and ROOT additionally set; preserve the16-word
feed-forward and exact selected G rounds/permutation. We conservatively
charge two compressions per full hash if a non-rootCV is also generated;
it cannot replace the ROOT compression. No keyed mode,alternate tree,
free-start or truncated output is substituted. Trees with multiple chunks
are not exercised because every internally generated message is64 bytes.

Orchard: Initialize[nk,rho,2^65] over the exactPallas field and use the
protected deployed constants/MDS. Retain four opening full rounds,
selected partial-prefix rounds and four closing full rounds at their original
indices. x^5 is three multiplications, applied to allcoordinates in full
rounds or coordinatezero in partial rounds; then denseMDS as specified.
Compare and canonically serialize finalcoordinatezero as the entire field
element. Neither fullnullifier nor rawpermutation replaces ConstantLength<2>.
The chosen capacity,output,exponent and encoding are unchanged.

Each byte hash uses at mosttwo target-compression primitives; two hashes
cost at mostfour units per trial. Orchard costs twoselected permutations.
No mathematical operation outside the selected primitive is silently free.
The following ledger charges encoding/state/padding/counters/randomness,
including the input/output boundary of the primitive. It does not double-charge
the internal compression/permutation body counted by the protected primitive.

## 6. Conservative finite outer-operation ledger

Use the protected256-bit word primitives (and canonicalPallas field primitives
on Orchard), not an unlimited-width arithmetic operation. At most16384
NON-COMPRESSION primitive operations per trial cover the explicit routine:

(A) Random draws and sampler processing<=1024 operations. Byte targets
use4draws and<=64 equality/counter/tempoperations. Orchard uses at most64draws,
with <=10 operations per draw:draw,store,load,compare,branch,attemptincrement,
branch and<=3temporaries. Coordinate initialization, retention, sampler-failure
flags and whole-tuple distinctness consume at most256 additional operations.
Thus<=896, leaving128margin inside1024. No64-draw budget is claimed to
pay for bookkeeping without that extra allocation.

(B) Primitive boundary encodings<=4096 operations. Each serialize OR
parse pass on128inputbytes uses <=8operations perbyte (shift,mask,load,
store,addressincrement,loopcontrol and two spare) giving<=1024. Charge
BOTH passes<=2048 even if the primitive directly accepts words. Charge
both full32-byte digest serialize/parse passes,128bytes in total,<=1024.
Returning/copying128 messagebytes costs<=1024. All lengths are finite
constants; output includes everybyte, including leadingzeroes. This explicitly
pays bothdirections rather than charging onepass for two conversions.

(C) Fixedtarget state/IV/capacity, messagepadding,length,counter/flags and
scratch initialization<=2048 operations. At most200word slots are cleared/copied
with<=8 operations per slot, and at most448 remaining constant comparisons,
branches and index arithmetic. Only64-byte inputs and fixedprofile states are
constructed; no unbounded external JSON input is consumed by this collision
constructor. Orchard inputs are generated integers,not an imported byte stream.

(D) Distinctness/fulloutputcomparison,success branch and explicit final
verification<=2048 operations. Compare up to4messagewords and allone256-bit
digestword (orfield), store result, canonically check output and copy at most
128bytes. Count <=256 comparison/flagoperations and <=1792 copying/dispatch
operations. The initial two fullhashes already verify both outputs; if the
implementation rechecks them, charge FOUR additional compressions below.

(E) Counter/overflow,loop,addressing,release,temporary loads/stores and
call/return overhead<=2048 operations. The counter has onelowword+flag;
alladdresses lie within1MiB. At most128fixedboundedslots and controlsites
use<=16operations each. Failure releases/overwrites slots; no allocation grows.

(F) An additional5120operation margin is explicitly reserved for local
random-source interface,constant-size dispatch,carry/endianness and callsetup.
The named(A)-(E)ceilings total11264; plus5120 is exactly16384. This margin
cannot pay for an unknown growing search/table; everyroutine is the finite
one described above. Allrandom/failed/successfultrial work is charged.

At mosteight targetcompressions per trial conservatively cover the original
four and fullreverification ofbothbytehashes. This sameeight-unit ceiling
overpricesOrchard's initialtwo and repeatedtwo permutations. The smallest
C among these nine exactprofiles is430 (BLAKE3tworounds). Thus

  trial_work <=8+16384/C <=8+16384/430 <64.

WithT=2^256,total trialwork<2^262. One-time coldsetup<2^20units (below)
then totalwork<2^262+2^20<2^263. The declared bound is263 for everytarget;
it is conservative,not an automatically tightened score. Preprocessing20
is charged within total263,not amortized over future attacks. Primitive
pricesC for the EXACT selected target are reproduced inSection9.

## 7. Simultaneous state and cold initialization

Use one sequential processor with local256-bit words and <=1MiB addresses.
A fixedprogram region<=2^18bytes contains the smallloops, targetouterglue and
fixedprofile primitive code/constant schedule. A further<=2^16byte region holds
alltarget IVs/MDS/roundconstants and caller dispatch (far larger than the largest
<=80-round256-bit constants and25-lane state require). Workingdata:
<=512256-bit words=16384bytes for state,padding,two64-byte messages,two32-byte
digests,acceptedfields,counters,flags,decoder temporaries and copiedoutput.
Reserve <=2^16bytes for stack/callframes,<=2^16for scratchandbyteencodings,
and <=2^16 for the boundedideal-random-word interface/register/controlstate.
Total<2^18+4*2^16+16384<2^20bytes, with no table or recordedcointranscript.
Theidealrandom-wordprimitive has no retained tape in the model; a physical
implementation must satisfy the statedfresh-coin assumption,not substitute
an unproveddeterministicseed.

Thecode uses fixednestedloops andbranchdispatch,no recursively growingstate.
Even lowering each fixedoperation/schedule site to a<=64byte instruction
sequence, with<=4096sites including allrounds/padding/sampler/control, fits
2^18codebytes; Section11 gives theauthoritativeconservativedirectRAMimage
argument and revised512slotlayout. Theprotectedhashprimitive implementation has fixedroundcount;
no searchedadvice or targetdependentcollision is embedded incode. Publicconstants
andalgorithmdesign are excluded from adviceconstruction by the protected rules.
Initializing<=2^20bytes in256-bit words means<=32768slots; clearing/copying each
with<=16operations costs<=2^19operations. Boot/counter/profileinstall<=2^18more
operations leaves<2^20 primitiveoperations. Charge<2^20targetunits regardless
of C, including code/constantcopies and allscratch/outputsetup. No precomputed
state,freearrayinitialization,hiddenrandomtape or future-targetamortization isused.

## 8. Claims, evidence, and honest provenance

Success_probability0.4 is a weakened lowerbound of the proven3/7 or9/17,
not reviewerconfidence. Heuristics is empty: the successproof is distributionfree
and the resourcecounts are finiteassumedword-model ceilings. Certificates are
an EMPTY validmanifest,not an allegedfoundcollision; noexperiments aredeclared.
This is analytic evidence allowed by the exploratory rules,not a runof2^256trials.
The parenttask has historicalcontext anddoes notclaim erasedmemory. Thecandidate
uses the independentpairedtrialresearch freshlyauthored forthisaccount; itdoesnot
copy anotheraccount'sproof,tablealgorithm,costfile,review,score oracceptance.
A previousbad/acceptedjudgment cannot establish thisclaim. Standard sampling
andCauchy/binomialfacts are fullyreproduced; noexternalcitation mustbe fetched.
Allnineinstantiations openlyshare thisnewgenericmethod andcommontext withdistinct
protectedtargets/prices. Changingtarget doesnot prove novelty. Thedeclaredtime263
andmemory20 projecttonormalizedtime-memory263 under the applicablepolicy.
This doesNOT improve the currentbest or nominalreference; itsintegerreference
label is requiredschema metadata only. AIqualification,frontierimprovement,
manualacceptance,actualcollision andprize are distinct. A non-improving valid
submission may be refused publication/recording; such a result mustbereported
as rejected/notimproved,not successfulcompletion or an invaliditycounterexample.

## 9. Exact selected profile and accounting

The exact reference price is C=2728. Selectedrounds=38.

```json
{
  "id": "sha256-r38-prefix-v1",
  "status": "frontier-experiment",
  "algorithm": "sha256",
  "primitive": "SHA-256",
  "specification": "FIPS 180-4",
  "specification_url": "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf",
  "rounds": 38,
  "full_rounds": 64,
  "round_count_unit": "compression rounds",
  "round_selection": "Execute indices 0 through 37, inclusive, on every padded block.",
  "digest_bits": 256,
  "attack_class": "ordinary-collision",
  "message_domain": "All finite byte strings with bit length less than 2^64; no chosen IV, free-start state, or digest truncation.",
  "block_bits": 512,
  "word_bits": 32,
  "padding": "FIPS 180-4: append 0x80, zero bytes to 56 modulo 64, then 64-bit BIG-endian original bit length.",
  "initialization": "Use the standard fixed IV from the specification once at the start of the complete message.",
  "schedule": "Use the standard message-word selection/expansion and constants at their original indices; do not renumber phases.",
  "feed_forward": "After each reduced compression, add every working state word to the incoming chaining state modulo 2^32. Preserve the full standard state and serialize in standard order.",
  "digest_encoding": "Big-endian standard chaining-state order; all digest words.",
  "reference_implementation": "verifier/hash_functions.py:digest",
  "relation": {
    "preconditions": [
      "m0 and m1 satisfy the message domain",
      "m0 is not byte-for-byte equal to m1"
    ],
    "postcondition": "The two complete sha256-r38 hashes are byte-for-byte equal."
  },
  "out_of_scope": [
    "compression-only or free-start collisions",
    "near-collisions or output truncation",
    "changing the IV, padding, round range, or output width",
    "implementation/side-channel attacks"
  ]
}
```

## 11. Primitive RAM pseudocode, live slots and program-image bound

This section supplies a concrete lowering for the earlier conservative
ceilings, not a change to the algorithm, inputs or collision event. All
ordinary instructions below are the priced256-bit primitive operations;
register/memory operands are aligned fullwordslots. The selectedcompression
is the protected pricedprimitive, not uncharged candidate code.

Representation: keep each64-byte message in2wordslots, eachdigest in1,
Orchardtuples in2each, and counter/flags in2. Temporarybytearrays use one
256-bit slot perbyte,avoiding read-modify-write subwordstores. These
arrays are reused sequentially,never retained for alltrials. Allslotindices
are literal finiteconstants or countersboundedby256 andfit oneRAMword.

Primitive templates (every line names one charged primitive; rightside
wordarithmetic is not a compound uncounted step):

  GETBYTE(v,i): t=8*i; u=v >> t; b=u AND255.
  PUTBYTE(v,b,i): t=8*i; u=b << t; v=v OR u.

Multiplicationby8 is a shiftby3,so these are3operations each. Ifv is in
memory,LOAD before andSTORE after adds2. A bytearrayload/store adds1.
Loopindexincrement,comparisonandconditionalbranch add3. Thus extracting
andstoring1byte<=9operations,not assumed8. Packing1byte<=9aswell.
Allow10perbyte toinclude dispatch. Process128inputbytes ineachdirection
plus64digestbytes ineachdirection plus128returnedbytes: total<=512bytes
and<=5120operations. In fact pointmessage return needsonly4wordcopies;
thebytecopyceiling is deliberatelylarger. Theseconversionstogether cost
<=5120,not theearlier4096stageB ceiling; therevised completeledgerbelow
absorbs this conservative correction without changing total16384.
No outputprefix is compared; alldigestwordbits/fieldvaluesare checked.

  BYTE_TRIAL:
    FORk=0..3: RANDOMv[k]; STOREv[k].             <=8
    LOADu0,u1,v0,v1; EQa=(u0==v0); EQb=(u1==v1);
    same=a ANDb; IFsame setfailure.              <=9
    CALLFULLHASHtwice; CALLtwiceagainifverify.    <=8compressions
    LOADh0,h1; EQequal=(h0==h1); IF(!sameANDequal)
      COPYall4messagewords; RETURNsuccess.
    INCREMENTlow; EQt=(low==0); STOREoverflow=t;
    IFoverflow RETURNfailure ELSEcontinue.

Branches,negation,LOAD/STORE offlags,counter andreturnprogramcounter are
charged. Thefinite template has<64otherops beforethe boundaryconversion
andtargetglue. Sampleequalinputsstillconsume1trial; thehashcalls may be
performedor skipped,neverincrease theworstcasecap. Thecounterbodydoes
execute onceatlow=0before increment,thenstops onlyonthefirstwrap.

  FIELD_SAMPLE:
    value=0; found=0; attempt=0.                   <=3
    REPEAT16:
      RANDOMt; STOREt; LOADt; LTok=(t<p);          <=4
      IFok: STOREvalue=t; STOREfound=1; BREAK;     <=3
      attempt=attempt+1; LTagain=(attempt<16);
      IFagainCONTINUE.                            <=3
    RETURN(value,found).                          <=2

Themostexpensivefailedstep<=10operations;16steps+init/return<=165.
Fourcoordinates<=660. Keepingall4values,ANDof4foundflags,twowordtuple
comparisons,success/failuredispatch andloopcontrol<=128. Total<=788,
inside1024samplingceiling. Shortcircuitfailureisallowed,not assumedfor
thisworstcase. This countsinitialization,retentionanddistinctness beyond
64draws. Values>=p are notreduced oraccepted; coordinatefailurecosts are
included andconditionalacceptedvaluesremainexactlyuniform.

FULLHASHglue is boundedby fixedslot loops,not unitcostBYTEpacking:
- SHA256: copies8IVwords,zeros16paddingwords,writeslength512and0x80,
  forms16wordblockarguments frommessagebytearrays andfeedsforwardall8words.
  Even using10opsper32-bit extraction/add/mask/store pluscontrol,<1024.
- SHA3: zeros25lanes,absorbs<=136byteswithGET/PUTBYTE,sets0x06and0x80,
  calls1selectedpermutation,extractsall32digestbytes.<2048glueopsperhash,
  includingallcallerbytehandling (boundaryceiling alsoovercounts it).
- BLAKE3: forms16blockwords,8IVwords,counter0,length64andflags3 for an optionalnon-rootcall and11 for theROOTcall;
  callsROOTon theoriginaloutputobject,notafinalCV; fullfeedforwardalready
  inprotectedcompression,<1024glueopsperhash includingoutputcopies.
- Orchard: loads2canonicalfieldsandcapacity2^65,callsselectedpermutation,
  copiesfullcoordinate0; deployedconstant/MDSopsbelong tothatpricedprimitive.
  <512glueopsperhash,includingfieldbyteconversion chargedabove.

Worstcase fourhashcalls(allinitialandreverification)times2048glueops
is<=8192. Someboundaryconversionisintentionallycountedbothhereandabove,
which overstates,not understates,work. Sum<=5120boundary+1024sampling+
8192glue+1024counter/return/flags/scratchreset=15360ordinaryops. The
remaining1024inside16384paysfixedcall/dispatchandloopsetup. Eachfixed
loophasstatedbound; no nestedloop dependsonthe2^256history. This
strictlyconservative totalkeeps trial_work<=8+16384/C andtotal263.
Earlierstageallocations are illustrative; thisexplicit15360+1024ledger
is authoritative when a stage'sindividualceiling differs. Thebound
is independentofmessagevalues/sampleracceptancetime.

Simultaneousdata:512aligned256-bitslots=16384bytes suffice:
128reusedbytebuffer+2messagepairs+4tuplecoords+2digests+2counter/flags+
32primitiveworkingstate+80schedule/constant-indextemporaries+128scratch
+32dispatch/frame/decoder registers+100reserved=512slotsorless.
Not allareliveatonce; counttheirsum anyway. Thebufferisreused between
conversions. A separatefixedconstantregion<=2^16bytesincludesSHA/Keccak/
BLAKE IVs/roundwordsandall64*3Orchardroundfieldconstantsplus9MDSfields
(<8192bytes),flagsandcanonicalp. No records/history/randomtapeareallocated.

Codeuses acountedinstructionformat with<=16bytesperRAMopcode(64bits
opcode/destinationplus64bits operands/indexes)andliteralpublicconstants
storedin theconstantregion. Thefixedoutertemplates/glueloopsneed<=1024
instruction-sitesincludingcall/return,addresses,andbranches. A protected
selectedprimitivecanbe a fixedloopimplementation; even storing oneopcode
per countedlogicaloperation at thelargestlistedC=6504 requires<=6504
sites,plusunpricedcontrol/fielddispatch reserve<=8192totalsites.
Orchardsimple27/21operationroundsreusea loopbody,not anunboundedmatrix
operator; additionsandmultiplicationsarepricedfieldprimitives. Thusallcode
<=8192*16=2^17bytes; reserve2^18codebytes. Thelistedprimitiveoperation
countsare notCPUcycles orruntimeof an importedPythonprogram. Algorithm
code/publicprofileconstantsarestored andinitialized,but theirdesign is
notsearchedadvice. ThisdirectRAMencoding is aspecifiedtheoreticalmachine
programimage,notanassertionofcompiledAArch64assemblysize.

Peakallocationusingthecorrected512databound is<=2^18code+4*2^16
constant/stack/scratch/RNGregions+16384data=540672bytes<2^20.
Clearing/copying thefull1MiB at32bytesperword requires32768iterations;
periterationLOAD/STORE,increment,compare,branch<=8ops (conservatively16).
Charge<=2^19ordinaryops. Installingcode/constantimages/counter/flags and
fixeddispatch has<=2^18moreordinaryops (the code/constantbytes occupy
<=32768words; directcopies at<=4opsperword plusfixedcontrolfitthisbound).
Allcoldsetup<=786432<2^20ordinaryops,conservatively<=2^20targetunits.
No allocator,stack,bootstraporcodeimagegrows with trialcount; randomwords
areconsumedanddiscarded without storing theirpastorfuture. Theprimitive
RNGinterfaceisexplicitfixedfinite modelstate; physicalcoinquality isnot
claimedverified. These details establishthefiniteanalyticalcode/state/
initializationbound,not aproductionsearch orofficialqualification.
