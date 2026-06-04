# baby-bof

## Description

Cod

## Initial vulnerability

## CHOP

Compile `ehdump` tool: https://github.com/chop-project/chop/tree/main/tools/ehdump

And use it to dump `try` block `start` and `end` addresses and `lp` - start of the `catch` block. 

```shell
ehdump ./index.cgi | head -n -1 | jq '.[].lsda.cses[] | select(any(.actions[]?; .ar_disp==0)) | {start,end,lp}'
```

```json
{
  "start": "0x4025a7",
  "end": "0x4025ac",
  "lp": "0x402632"
}
{
  "start": "0x4036c7",
  "end": "0x4036cc",
  "lp": "0x403758"
}
{
  "start": "0x4037a1",
  "end": "0x4037a6",
  "lp": "0x4037a6"
}
{
  "start": "0x4037c8",
  "end": "0x4037ca",
  "lp": "0x4037cf"
}
{
  "start": "0x4012b4",
  "end": "0x4012b9",
  "lp": "0x40124d"
}
{
  "start": "0x404b96",
  "end": "0x404b9b",
  "lp": "0x404bd3"
}
{
  "start": "0x407d0b",
  "end": "0x407d10",
  "lp": "0x407d7c"
}
{
  "start": "0x40a415",
  "end": "0x40a4c5",
  "lp": "0x40a4ef"
}
```
