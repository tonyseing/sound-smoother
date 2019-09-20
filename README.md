# sound-smoother
Sound filter that smooths audio input

In this exercise, we will implement a simple approach to downsample an audio signal by a factor
of two. Changing the sample rate is one of the most common data permutations taken when
working with audio data, and specifically this exercise will describe how to accomplish this using
a specific kind of low pass filter across the audio data, and then performing decimation.

![](https://github.com/tonyseing/sound-smoother/blob/master/images/lowpass.png?raw=true)

![](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4NCjxzdmcgdmVyc2lvbj0iMS4x%0D%0AIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8v%0D%0Ad3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiB2aWV3Qm94%0D%0APSIwIDAgNjQwIDQ4MCI+DQogPHRpdGxlPmNvbXBhcmlzb24gY29udm9sdXRpb24gY29ycmVsYXRp%0D%0Ab248L3RpdGxlPg0KIDxkZXNjPlZpc3VhbCBjb21wYXJpc29uIG9mIGNvbnZvbHV0aW9uLCBjcm9z%0D%0Acy1jb3JyZWxhdGlvbiBhbmQgYXV0b2NvcnJlbGF0aW9uIG9mIHR3byBzaWduYWxzIGJ5IENNRyBM%0D%0AZWUuPC9kZXNjPg0KIDxzdHlsZSB0eXBlPSJ0ZXh0L2NzcyI+DQogIHRleHQgeyBmaWxsOiMwMDAw%0D%0AMDA7IH0NCiAgI2dyYXBoX2dnLCNncmFwaF9nZiwjZ3JhcGhfZmYgeyBzdHJva2U6IzAwMDAwMDsg%0D%0AfQ0KICAjZ3JhcGhfZiAgeyBzdHJva2U6IzAwMDBmZjsgfQ0KICAjZ3JhcGhfZyAgeyBzdHJva2U6%0D%0AI2ZmMDAwMDsgfQ0KICAucG9pbnRfMSAgeyBzdHJva2U6I2NjOTkwMDsgZmlsbDojY2M5OTAwOyB9%0D%0ADQogIC5wb2ludF8yICB7IHN0cm9rZTojMDBjYzAwOyBmaWxsOiMwMGNjMDA7IH0NCiAgLnBvaW50%0D%0AXzMgIHsgc3Ryb2tlOiMwMDk5Y2M7IGZpbGw6IzAwOTljYzsgfQ0KICAjcG9pbnRlcnMgeyBzdHJv%0D%0Aa2U6Izk5OTk5OTsgZmlsbDojOTk5OTk5OyB9DQogPC9zdHlsZT4NCiA8ZGVmcz4NCiAgPHBhdGgg%0D%0AaWQ9ImFycm93aGVhZCIgZD0iTSAtMywyIEwgMCwtMSBMIDMsMiIgc3Ryb2tlPSJub25lIi8+DQog%0D%0AIDxnIGlkPSJhcnJvd18xIiB0cmFuc2Zvcm09InNjYWxlKDIpIj48cGF0aCBkPSJNIDAsMCBWICAt%0D%0ANSIvPjx1c2UgeGxpbms6aHJlZj0iI2Fycm93aGVhZCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCwg%0D%0ALTUpIi8+PHVzZSB4bGluazpocmVmPSIjYXJyb3doZWFkIiB0cmFuc2Zvcm09InNjYWxlKC0xKSIv%0D%0APjwvZz4NCiAgPGcgaWQ9ImFycm93XzMiIHRyYW5zZm9ybT0ic2NhbGUoMikiPjxwYXRoIGQ9Ik0g%0D%0AMCwwIFYgLTE1Ii8+PHVzZSB4bGluazpocmVmPSIjYXJyb3doZWFkIiB0cmFuc2Zvcm09InRyYW5z%0D%0AbGF0ZSgwLC0xNSkiLz48dXNlIHhsaW5rOmhyZWY9IiNhcnJvd2hlYWQiIHRyYW5zZm9ybT0ic2Nh%0D%0AbGUoLTEpIi8+PC9nPg0KICA8ZyBpZD0iYXJyb3dfNCIgdHJhbnNmb3JtPSJzY2FsZSgyKSI+PHBh%0D%0AdGggZD0iTSAwLDAgViAtMjAiLz48dXNlIHhsaW5rOmhyZWY9IiNhcnJvd2hlYWQiIHRyYW5zZm9y%0D%0AbT0idHJhbnNsYXRlKDAsLTIwKSIvPjx1c2UgeGxpbms6aHJlZj0iI2Fycm93aGVhZCIgdHJhbnNm%0D%0Ab3JtPSJzY2FsZSgtMSkiLz48L2c+DQogIDxnIGlkPSJhcnJvd184IiB0cmFuc2Zvcm09InNjYWxl%0D%0AKDIpIj48cGF0aCBkPSJNIDAsMCBWIC00MCIvPjx1c2UgeGxpbms6aHJlZj0iI2Fycm93aGVhZCIg%0D%0AdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCwtNDApIi8+PHVzZSB4bGluazpocmVmPSIjYXJyb3doZWFk%0D%0AIiB0cmFuc2Zvcm09InNjYWxlKC0xKSIvPjwvZz4NCiAgPGcgaWQ9InBvaW50ZXJzIiBzdHJva2Ut%0D%0Ad2lkdGg9IjEiPg0KICAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTQwLDApIj4NCiAgICA8cGF0%0D%0AaCBkPSJNIDAgNSBWIDM1Ii8+DQogICAgPHVzZSB4bGluazpocmVmPSIjYXJyb3doZWFkIiB0cmFu%0D%0Ac2Zvcm09InRyYW5zbGF0ZSgwLDUpIi8+DQogICA8L2c+DQogICA8ZyB0cmFuc2Zvcm09InRyYW5z%0D%0AbGF0ZSgtMjAsMCkiPg0KICAgIDxwYXRoIGQ9Ik0gMCA1IFYgNjUiLz4NCiAgICA8dXNlIHhsaW5r%0D%0AOmhyZWY9IiNhcnJvd2hlYWQiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAsNSkiLz4NCiAgIDwvZz4N%0D%0ACiAgIDxnPg0KICAgIDxwYXRoIGQ9Ik0gMCA1IFYgNzUiLz4NCiAgICA8dXNlIHhsaW5rOmhyZWY9%0D%0AIiNhcnJvd2hlYWQiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAsNSkiLz4NCiAgIDwvZz4NCiAgIDxn%0D%0AIHRyYW5zZm9ybT0idHJhbnNsYXRlKDIwLDApIj4NCiAgICA8cGF0aCBkPSJNIDAgNSBWIDY1Ii8+%0D%0ADQogICAgPHVzZSB4bGluazpocmVmPSIjYXJyb3doZWFkIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgw%0D%0ALDUpIi8+DQogICA8L2c+DQogICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSg0MCwwKSI+DQogICAg%0D%0APHBhdGggZD0iTSAwIDUgViAzNSIvPg0KICAgIDx1c2UgeGxpbms6aHJlZj0iI2Fycm93aGVhZCIg%0D%0AdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCw1KSIvPg0KICAgPC9nPg0KICA8L2c+DQogIDxwYXRoIGlk%0D%0APSJncmFwaF9mIiAgZD0iTSAtNTUsMCBIIC0xMCBWIC0yMiBWIC0yMCBIIDEwIFYgMCBIIDU1Ii8+%0D%0ADQogIDxwYXRoIGlkPSJncmFwaF9nIiAgZD0iTSAtNTUsMCBIIC0xMCAgICAgICBWIC0yMCBMIDEw%0D%0ALDAgICBIIDU1Ii8+DQogIDxwYXRoIGlkPSJncmFwaF9nZyIgZD0iTSAtNTUsMCBIIC0yMCBRIC0x%0D%0AMCwgIDAgMCwtMjAgUSAxMCwgIDAgMjAsMCBIIDU1Ii8+DQogIDxwYXRoIGlkPSJncmFwaF9nZiIg%0D%0AZD0iTSAtNTUsMCBIIC0yMCBRIC0xMCwgIDAgMCwtMjAgUSAxMCwtMjAgMjAsMCBIIDU1Ii8+DQog%0D%0AIDxwYXRoIGlkPSJncmFwaF9mZiIgZD0iTSAtNTUsMCBIIC0yMCBMICAgICAgICAgMCwtNDAgTCAg%0D%0AICAgICAgMjAsMCBIIDU1Ii8+DQogIDx1c2UgIGlkPSJncmFwaF9mX3JldiIgICAgIHhsaW5rOmhy%0D%0AZWY9IiNncmFwaF9mIiAgICAgdHJhbnNmb3JtPSJzY2FsZSgtMSwxKSIvPg0KICA8dXNlICBpZD0i%0D%0AZ3JhcGhfZ19yZXYiICAgICB4bGluazpocmVmPSIjZ3JhcGhfZyIgICAgIHRyYW5zZm9ybT0ic2Nh%0D%0AbGUoLTEsMSkiLz4NCiAgPHVzZSAgaWQ9ImdyYXBoX2ZnIiAgICAgICAgeGxpbms6aHJlZj0iI2dy%0D%0AYXBoX2dmIiAgICB0cmFuc2Zvcm09InNjYWxlKC0xLDEpIi8+DQogIDx1c2UgIGlkPSJncmFwaF9i%0D%0AaWdfZiIgICAgIHhsaW5rOmhyZWY9IiNncmFwaF9mIiAgICAgdHJhbnNmb3JtPSJzY2FsZSgyKSIv%0D%0APg0KICA8dXNlICBpZD0iZ3JhcGhfYmlnX2ciICAgICB4bGluazpocmVmPSIjZ3JhcGhfZyIgICAg%0D%0AIHRyYW5zZm9ybT0ic2NhbGUoMikiLz4NCiAgPHVzZSAgaWQ9ImdyYXBoX2JpZ19mX3JldiIgeGxp%0D%0Abms6aHJlZj0iI2dyYXBoX2ZfcmV2IiB0cmFuc2Zvcm09InNjYWxlKDIpIi8+DQogIDx1c2UgIGlk%0D%0APSJncmFwaF9iaWdfZ19yZXYiIHhsaW5rOmhyZWY9IiNncmFwaF9nX3JldiIgdHJhbnNmb3JtPSJz%0D%0AY2FsZSgyKSIvPg0KICA8dXNlICBpZD0iZ3JhcGhfYmlnX2ZnIiAgICB4bGluazpocmVmPSIjZ3Jh%0D%0AcGhfZmciICAgIHRyYW5zZm9ybT0ic2NhbGUoMikiLz4NCiAgPHVzZSAgaWQ9ImdyYXBoX2JpZ19n%0D%0AZyIgICAgeGxpbms6aHJlZj0iI2dyYXBoX2dnIiAgICB0cmFuc2Zvcm09InNjYWxlKDIpIi8+DQog%0D%0AIDx1c2UgIGlkPSJncmFwaF9iaWdfZ2YiICAgIHhsaW5rOmhyZWY9IiNncmFwaF9nZiIgICAgdHJh%0D%0AbnNmb3JtPSJzY2FsZSgyKSIvPg0KICA8dXNlICBpZD0iZ3JhcGhfYmlnX2ZmIiAgICB4bGluazpo%0D%0AcmVmPSIjZ3JhcGhfZmYiICAgIHRyYW5zZm9ybT0ic2NhbGUoMikiLz4NCiAgPGNsaXBQYXRoIGlk%0D%0APSJjbGlwX2dyYXBoX2YiPjx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2YiLz48L2NsaXBQYXRoPg0K%0D%0AICA8Y2xpcFBhdGggaWQ9ImNsaXBfZ3JhcGhfZyI+PHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZyIv%0D%0APjwvY2xpcFBhdGg+DQogIDxjbGlwUGF0aCBpZD0iY2xpcF9wb2ludCI+PHJlY3QgeD0iLTM1IiB5%0D%0APSItMjUiICAgd2lkdGg9IjcwIiAgaGVpZ2h0PSIzMCIgIC8+PC9jbGlwUGF0aD4NCiAgPGNsaXBQ%0D%0AYXRoIGlkPSJjbGlwX3NldCIgID48cmVjdCB4PSItOTUiIHk9Ii00OTk5IiB3aWR0aD0iMTkwIiBo%0D%0AZWlnaHQ9Ijk5OTkiLz48L2NsaXBQYXRoPg0KIDwvZGVmcz4NCg0KIDxnIGZvbnQtZmFtaWx5PSJI%0D%0AZWx2ZXRpY2EsQXJpYWwsc2Fucy1zZXJpZiIgZm9udC1zaXplPSIyNCIgdGV4dC1hbmNob3I9Im1p%0D%0AZGRsZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBmaWxsPSJub25l%0D%0AIj4NCiAgPGNpcmNsZSBjeD0iMCIgY3k9IjAiIHI9Ijk5OTk5IiBmaWxsPSIjZmZmZmZmIi8+DQog%0D%0AIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDEwMCwyMykiIGNsaXAtcGF0aD0idXJsKCNjbGlwX3Nl%0D%0AdCkiPg0KICAgPHRleHQgeD0iMCIgeT0iMCI+Q29udm9sdXRpb248L3RleHQ+DQogICA8ZyB0cmFu%0D%0Ac2Zvcm09InRyYW5zbGF0ZSgwLCA2MCkiPjx0ZXh0IHg9Ii02NSIgeT0iLTIwIj5mPC90ZXh0Pjx1%0D%0Ac2UgeGxpbms6aHJlZj0iI2dyYXBoX2JpZ19mIi8+PC9nPg0KICAgPGcgdHJhbnNmb3JtPSJ0cmFu%0D%0Ac2xhdGUoMCwxMTApIj48dGV4dCB4PSItNjUiIHk9Ii0yMCI+ZzwvdGV4dD48dXNlIHhsaW5rOmhy%0D%0AZWY9IiNncmFwaF9iaWdfZyIvPjwvZz4NCiAgIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAsMTkw%0D%0AKSI+DQogICAgPHRleHQgeD0iLTY1IiB5PSItMjAiPmYmIzg3Mjc7ZzwvdGV4dD48dXNlIHhsaW5r%0D%0AOmhyZWY9IiNncmFwaF9iaWdfZmciLz4NCiAgICA8dXNlIHhsaW5rOmhyZWY9IiNhcnJvd18zIiBj%0D%0AbGFzcz0icG9pbnRfMSIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTIwLDApIi8+DQogICAgPHVzZSB4%0D%0AbGluazpocmVmPSIjYXJyb3dfNCIgY2xhc3M9InBvaW50XzIiIHRyYW5zZm9ybT0idHJhbnNsYXRl%0D%0AKCAgMCwwKSIvPg0KICAgIDx1c2UgeGxpbms6aHJlZj0iI2Fycm93XzEiIGNsYXNzPSJwb2ludF8z%0D%0AIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSggMjAsMCkiLz4NCiAgICA8dXNlIHhsaW5rOmhyZWY9IiNw%0D%0Ab2ludGVycyIvPg0KICAgIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKC02MCw0MCkiIGNsaXAtcGF0%0D%0AaD0idXJsKCNjbGlwX3BvaW50KSI+DQogICAgIDx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2YiLz4N%0D%0ACiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZ19yZXYiIHRyYW5zZm9ybT0idHJhbnNsYXRl%0D%0AKC0yMCwwKSIvPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9mIiBzdHJva2Utb3BhY2l0%0D%0AeT0iMC41Ii8+DQogICAgPC9nPg0KICAgIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKC00NSw3MCki%0D%0AIGNsaXAtcGF0aD0idXJsKCNjbGlwX3BvaW50KSI+DQogICAgIDxnIGNsaXAtcGF0aD0idXJsKCNj%0D%0AbGlwX2dyYXBoX2YpIj48dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9nX3JldiIgY2xhc3M9InBvaW50%0D%0AXzEiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMCwwKSIvPjwvZz4NCiAgICAgPHVzZSB4bGluazpo%0D%0AcmVmPSIjZ3JhcGhfZiIvPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9nX3JldiIgdHJh%0D%0AbnNmb3JtPSJ0cmFuc2xhdGUoLTEwLDApIi8+DQogICAgIDx1c2UgeGxpbms6aHJlZj0iI2dyYXBo%0D%0AX2YiIHN0cm9rZS1vcGFjaXR5PSIwLjUiLz4NCiAgICA8L2c+DQogICAgPGcgdHJhbnNmb3JtPSJ0%0D%0AcmFuc2xhdGUoMCwxMDApIiBjbGlwLXBhdGg9InVybCgjY2xpcF9wb2ludCkiPg0KICAgICA8dXNl%0D%0AIHhsaW5rOmhyZWY9IiNncmFwaF9mIi8+DQogICAgIDx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2df%0D%0AcmV2IiBjbGFzcz0icG9pbnRfMiIvPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9mIiBz%0D%0AdHJva2Utb3BhY2l0eT0iMC41Ii8+DQogICAgPC9nPg0KICAgIDxnIHRyYW5zZm9ybT0idHJhbnNs%0D%0AYXRlKDQ1LDcwKSIgY2xpcC1wYXRoPSJ1cmwoI2NsaXBfcG9pbnQpIj4NCiAgICAgPGcgY2xpcC1w%0D%0AYXRoPSJ1cmwoI2NsaXBfZ3JhcGhfZikiPjx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2dfcmV2IiBj%0D%0AbGFzcz0icG9pbnRfMyIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMTAsMCkiLz48L2c+DQogICAgIDx1%0D%0Ac2UgeGxpbms6aHJlZj0iI2dyYXBoX2YiLz4NCiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3JhcGhf%0D%0AZ19yZXYiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDEwLDApIi8+DQogICAgIDx1c2UgeGxpbms6aHJl%0D%0AZj0iI2dyYXBoX2YiIHN0cm9rZS1vcGFjaXR5PSIwLjUiLz4NCiAgICA8L2c+DQogICAgPGcgdHJh%0D%0AbnNmb3JtPSJ0cmFuc2xhdGUoNjAsNDApIiBjbGlwLXBhdGg9InVybCgjY2xpcF9wb2ludCkiPg0K%0D%0AICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9mIi8+DQogICAgIDx1c2UgeGxpbms6aHJlZj0i%0D%0AI2dyYXBoX2dfcmV2IiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgyMCwwKSIvPg0KICAgICA8dXNlIHhs%0D%0AaW5rOmhyZWY9IiNncmFwaF9mIiBzdHJva2Utb3BhY2l0eT0iMC41Ii8+DQogICAgPC9nPg0KICAg%0D%0APC9nPg0KICAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCwzNTApIj4NCiAgICA8dGV4dCB4PSIt%0D%0ANjUiIHk9Ii0yMCI+ZyYjODcyNztmPC90ZXh0Pjx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2JpZ19m%0D%0AZyIvPg0KICAgIDx1c2UgeGxpbms6aHJlZj0iI2Fycm93XzMiIGNsYXNzPSJwb2ludF8xIiB0cmFu%0D%0Ac2Zvcm09InRyYW5zbGF0ZSgtMjAsMCkiLz4NCiAgICA8dXNlIHhsaW5rOmhyZWY9IiNhcnJvd180%0D%0AIiBjbGFzcz0icG9pbnRfMiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoICAwLDApIi8+DQogICAgPHVz%0D%0AZSB4bGluazpocmVmPSIjYXJyb3dfMSIgY2xhc3M9InBvaW50XzMiIHRyYW5zZm9ybT0idHJhbnNs%0D%0AYXRlKCAyMCwwKSIvPg0KICAgIDx1c2UgeGxpbms6aHJlZj0iI3BvaW50ZXJzIi8+DQogICAgPGcg%0D%0AdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTYwLDQwKSIgY2xpcC1wYXRoPSJ1cmwoI2NsaXBfcG9pbnQp%0D%0AIj4NCiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZyIvPg0KICAgICA8dXNlIHhsaW5rOmhy%0D%0AZWY9IiNncmFwaF9mX3JldiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTIwLDApIi8+DQogICAgIDx1%0D%0Ac2UgeGxpbms6aHJlZj0iI2dyYXBoX2ciIHN0cm9rZS1vcGFjaXR5PSIwLjUiLz4NCiAgICA8L2c+%0D%0ADQogICAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTQ1LDcwKSIgY2xpcC1wYXRoPSJ1cmwoI2Ns%0D%0AaXBfcG9pbnQpIj4NCiAgICAgPGcgY2xpcC1wYXRoPSJ1cmwoI2NsaXBfZ3JhcGhfZykiPjx1c2Ug%0D%0AeGxpbms6aHJlZj0iI2dyYXBoX2ZfcmV2IiBjbGFzcz0icG9pbnRfMSIgdHJhbnNmb3JtPSJ0cmFu%0D%0Ac2xhdGUoLTEwLDApIi8+PC9nPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9nIi8+DQog%0D%0AICAgIDx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2ZfcmV2IiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgt%0D%0AMTAsMCkiLz4NCiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZyIgc3Ryb2tlLW9wYWNpdHk9%0D%0AIjAuNSIvPg0KICAgIDwvZz4NCiAgICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLDEwMCkiIGNs%0D%0AaXAtcGF0aD0idXJsKCNjbGlwX3BvaW50KSI+DQogICAgIDx1c2UgeGxpbms6aHJlZj0iI2dyYXBo%0D%0AX2ciIGNsYXNzPSJwb2ludF8yIi8+DQogICAgIDx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2ZfcmV2%0D%0AIi8+DQogICAgIDx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2ciIHN0cm9rZS1vcGFjaXR5PSIwLjUi%0D%0ALz4NCiAgICA8L2c+DQogICAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNDUsNzApIiBjbGlwLXBh%0D%0AdGg9InVybCgjY2xpcF9wb2ludCkiPg0KICAgICA8ZyBjbGlwLXBhdGg9InVybCgjY2xpcF9ncmFw%0D%0AaF9nKSI+PHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZl9yZXYiIGNsYXNzPSJwb2ludF8zIiB0cmFu%0D%0Ac2Zvcm09InRyYW5zbGF0ZSgxMCwwKSIvPjwvZz4NCiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3Jh%0D%0AcGhfZyIvPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9mX3JldiIgdHJhbnNmb3JtPSJ0%0D%0AcmFuc2xhdGUoMTAsMCkiLz4NCiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZyIgc3Ryb2tl%0D%0ALW9wYWNpdHk9IjAuNSIvPg0KICAgIDwvZz4NCiAgICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSg2%0D%0AMCw0MCkiIGNsaXAtcGF0aD0idXJsKCNjbGlwX3BvaW50KSI+DQogICAgIDx1c2UgeGxpbms6aHJl%0D%0AZj0iI2dyYXBoX2ciLz4NCiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZl9yZXYiIHRyYW5z%0D%0AZm9ybT0idHJhbnNsYXRlKDIwLDApIi8+DQogICAgIDx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2ci%0D%0AIHN0cm9rZS1vcGFjaXR5PSIwLjUiLz4NCiAgICA8L2c+DQogICA8L2c+DQogIDwvZz4NCg0KICA8%0D%0AZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgzMjAsMjMpIiBjbGlwLXBhdGg9InVybCgjY2xpcF9zZXQp%0D%0AIj4NCiAgIDx0ZXh0IHg9IjAiIHk9IjAiPkNyb3NzLWNvcnJlbGF0aW9uPC90ZXh0Pg0KICAgPGcg%0D%0AdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCwgNjApIj48dGV4dCB4PSItNjUiIHk9Ii0yMCI+ZjwvdGV4%0D%0AdD48dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9iaWdfZiIvPjwvZz4NCiAgIDxnIHRyYW5zZm9ybT0i%0D%0AdHJhbnNsYXRlKDAsMTEwKSI+PHRleHQgeD0iLTY1IiB5PSItMjAiPmc8L3RleHQ+PHVzZSB4bGlu%0D%0AazpocmVmPSIjZ3JhcGhfYmlnX2ciLz48L2c+DQogICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgw%0D%0ALDE5MCkiPg0KICAgIDx0ZXh0IHg9Ii02NSIgeT0iLTIwIj5nJiM4OTAyO2Y8L3RleHQ+PHVzZSB4%0D%0AbGluazpocmVmPSIjZ3JhcGhfYmlnX2dmIi8+DQogICAgPHVzZSB4bGluazpocmVmPSIjYXJyb3df%0D%0AMSIgY2xhc3M9InBvaW50XzEiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0yMCwwKSIvPg0KICAgIDx1%0D%0Ac2UgeGxpbms6aHJlZj0iI2Fycm93XzQiIGNsYXNzPSJwb2ludF8yIiB0cmFuc2Zvcm09InRyYW5z%0D%0AbGF0ZSggIDAsMCkiLz4NCiAgICA8dXNlIHhsaW5rOmhyZWY9IiNhcnJvd18zIiBjbGFzcz0icG9p%0D%0AbnRfMyIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoIDIwLDApIi8+DQogICAgPHVzZSB4bGluazpocmVm%0D%0APSIjcG9pbnRlcnMiLz4NCiAgICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNjAsNDApIiBjbGlw%0D%0ALXBhdGg9InVybCgjY2xpcF9wb2ludCkiPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9m%0D%0AIi8+DQogICAgIDx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2ciIHRyYW5zZm9ybT0idHJhbnNsYXRl%0D%0AKC0yMCwwKSIvPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9mIiBzdHJva2Utb3BhY2l0%0D%0AeT0iMC41Ii8+DQogICAgPC9nPg0KICAgIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKC00NSw3MCki%0D%0AIGNsaXAtcGF0aD0idXJsKCNjbGlwX3BvaW50KSI+DQogICAgIDxnIGNsaXAtcGF0aD0idXJsKCNj%0D%0AbGlwX2dyYXBoX2YpIj48dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9nIiBjbGFzcz0icG9pbnRfMSIg%0D%0AdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEwLDApIi8+PC9nPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9%0D%0AIiNncmFwaF9mIi8+DQogICAgIDx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2ciIHRyYW5zZm9ybT0i%0D%0AdHJhbnNsYXRlKC0xMCwwKSIvPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9mIiBzdHJv%0D%0Aa2Utb3BhY2l0eT0iMC41Ii8+DQogICAgPC9nPg0KICAgIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRl%0D%0AKDAsMTAwKSIgY2xpcC1wYXRoPSJ1cmwoI2NsaXBfcG9pbnQpIj4NCiAgICAgPHVzZSB4bGluazpo%0D%0AcmVmPSIjZ3JhcGhfZiIvPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9nIiBjbGFzcz0i%0D%0AcG9pbnRfMiIvPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9mIiBzdHJva2Utb3BhY2l0%0D%0AeT0iMC41Ii8+DQogICAgPC9nPg0KICAgIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDQ1LDcwKSIg%0D%0AY2xpcC1wYXRoPSJ1cmwoI2NsaXBfcG9pbnQpIj4NCiAgICAgPGcgY2xpcC1wYXRoPSJ1cmwoI2Ns%0D%0AaXBfZ3JhcGhfZikiPjx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2ciIGNsYXNzPSJwb2ludF8zIiB0%0D%0AcmFuc2Zvcm09InRyYW5zbGF0ZSgxMCwwKSIvPjwvZz4NCiAgICAgPHVzZSB4bGluazpocmVmPSIj%0D%0AZ3JhcGhfZiIvPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9nIiB0cmFuc2Zvcm09InRy%0D%0AYW5zbGF0ZSgxMCwwKSIvPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9mIiBzdHJva2Ut%0D%0Ab3BhY2l0eT0iMC41Ii8+DQogICAgPC9nPg0KICAgIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDYw%0D%0ALDQwKSIgY2xpcC1wYXRoPSJ1cmwoI2NsaXBfcG9pbnQpIj4NCiAgICAgPHVzZSB4bGluazpocmVm%0D%0APSIjZ3JhcGhfZiIvPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9nIiB0cmFuc2Zvcm09%0D%0AInRyYW5zbGF0ZSgyMCwwKSIvPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9mIiBzdHJv%0D%0Aa2Utb3BhY2l0eT0iMC41Ii8+DQogICAgPC9nPg0KICAgPC9nPg0KICAgPGcgdHJhbnNmb3JtPSJ0%0D%0AcmFuc2xhdGUoMCwzNTApIj4NCiAgICA8dGV4dCB4PSItNjUiIHk9Ii0yMCI+ZiYjODkwMjtnPC90%0D%0AZXh0Pjx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2JpZ19mZyIvPg0KICAgIDx1c2UgeGxpbms6aHJl%0D%0AZj0iI2Fycm93XzMiIGNsYXNzPSJwb2ludF8xIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMjAsMCki%0D%0ALz4NCiAgICA8dXNlIHhsaW5rOmhyZWY9IiNhcnJvd180IiBjbGFzcz0icG9pbnRfMiIgdHJhbnNm%0D%0Ab3JtPSJ0cmFuc2xhdGUoICAwLDApIi8+DQogICAgPHVzZSB4bGluazpocmVmPSIjYXJyb3dfMSIg%0D%0AY2xhc3M9InBvaW50XzMiIHRyYW5zZm9ybT0idHJhbnNsYXRlKCAyMCwwKSIvPg0KICAgIDx1c2Ug%0D%0AeGxpbms6aHJlZj0iI3BvaW50ZXJzIi8+DQogICAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTYw%0D%0ALDQwKSIgY2xpcC1wYXRoPSJ1cmwoI2NsaXBfcG9pbnQpIj4NCiAgICAgPHVzZSB4bGluazpocmVm%0D%0APSIjZ3JhcGhfZyIvPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9mIiB0cmFuc2Zvcm09%0D%0AInRyYW5zbGF0ZSgtMjAsMCkiLz4NCiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZyIgc3Ry%0D%0Ab2tlLW9wYWNpdHk9IjAuNSIvPg0KICAgIDwvZz4NCiAgICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0%0D%0AZSgtNDUsNzApIiBjbGlwLXBhdGg9InVybCgjY2xpcF9wb2ludCkiPg0KICAgICA8ZyBjbGlwLXBh%0D%0AdGg9InVybCgjY2xpcF9ncmFwaF9nKSI+PHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZiIgY2xhc3M9%0D%0AInBvaW50XzEiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMCwwKSIvPjwvZz4NCiAgICAgPHVzZSB4%0D%0AbGluazpocmVmPSIjZ3JhcGhfZyIvPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9mIiB0%0D%0AcmFuc2Zvcm09InRyYW5zbGF0ZSgtMTAsMCkiLz4NCiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3Jh%0D%0AcGhfZyIgc3Ryb2tlLW9wYWNpdHk9IjAuNSIvPg0KICAgIDwvZz4NCiAgICA8ZyB0cmFuc2Zvcm09%0D%0AInRyYW5zbGF0ZSgwLDEwMCkiIGNsaXAtcGF0aD0idXJsKCNjbGlwX3BvaW50KSI+DQogICAgIDx1%0D%0Ac2UgeGxpbms6aHJlZj0iI2dyYXBoX2ciIGNsYXNzPSJwb2ludF8yIi8+DQogICAgIDx1c2UgeGxp%0D%0Abms6aHJlZj0iI2dyYXBoX2YiLz4NCiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZyIgc3Ry%0D%0Ab2tlLW9wYWNpdHk9IjAuNSIvPg0KICAgIDwvZz4NCiAgICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0%0D%0AZSg0NSw3MCkiIGNsaXAtcGF0aD0idXJsKCNjbGlwX3BvaW50KSI+DQogICAgIDxnIGNsaXAtcGF0%0D%0AaD0idXJsKCNjbGlwX2dyYXBoX2cpIj48dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9mIiBjbGFzcz0i%0D%0AcG9pbnRfMyIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMTAsMCkiLz48L2c+DQogICAgIDx1c2UgeGxp%0D%0Abms6aHJlZj0iI2dyYXBoX2ciLz4NCiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZiIgdHJh%0D%0AbnNmb3JtPSJ0cmFuc2xhdGUoMTAsMCkiLz4NCiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3JhcGhf%0D%0AZyIgc3Ryb2tlLW9wYWNpdHk9IjAuNSIvPg0KICAgIDwvZz4NCiAgICA8ZyB0cmFuc2Zvcm09InRy%0D%0AYW5zbGF0ZSg2MCw0MCkiIGNsaXAtcGF0aD0idXJsKCNjbGlwX3BvaW50KSI+DQogICAgIDx1c2Ug%0D%0AeGxpbms6aHJlZj0iI2dyYXBoX2ciLz4NCiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZiIg%0D%0AdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMjAsMCkiLz4NCiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3Jh%0D%0AcGhfZyIgc3Ryb2tlLW9wYWNpdHk9IjAuNSIvPg0KICAgIDwvZz4NCiAgIDwvZz4NCiAgPC9nPg0K%0D%0ADQogIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDU0MCwyMykiIGNsaXAtcGF0aD0idXJsKCNjbGlw%0D%0AX3NldCkiPg0KICAgPHRleHQgeD0iMCIgeT0iMCI+QXV0b2NvcnJlbGF0aW9uPC90ZXh0Pg0KICAg%0D%0APGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCwgNjApIj48dGV4dCB4PSItNjUiIHk9Ii0yMCI+Zjwv%0D%0AdGV4dD48dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9iaWdfZiIvPjwvZz4NCiAgIDxnIHRyYW5zZm9y%0D%0AbT0idHJhbnNsYXRlKDAsMTEwKSI+PHRleHQgeD0iLTY1IiB5PSItMjAiPmc8L3RleHQ+PHVzZSB4%0D%0AbGluazpocmVmPSIjZ3JhcGhfYmlnX2ciLz48L2c+DQogICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0%0D%0AZSgwLDE5MCkiPg0KICAgIDx0ZXh0IHg9Ii02NSIgeT0iLTIwIj5mJiM4OTAyO2Y8L3RleHQ+PHVz%0D%0AZSB4bGluazpocmVmPSIjZ3JhcGhfYmlnX2ZmIi8+DQogICAgPHVzZSB4bGluazpocmVmPSIjYXJy%0D%0Ab3dfNCIgY2xhc3M9InBvaW50XzEiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0yMCwwKSIvPg0KICAg%0D%0AIDx1c2UgeGxpbms6aHJlZj0iI2Fycm93XzgiIGNsYXNzPSJwb2ludF8yIiB0cmFuc2Zvcm09InRy%0D%0AYW5zbGF0ZSggIDAsMCkiLz4NCiAgICA8dXNlIHhsaW5rOmhyZWY9IiNhcnJvd180IiBjbGFzcz0i%0D%0AcG9pbnRfMyIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoIDIwLDApIi8+DQogICAgPHVzZSB4bGluazpo%0D%0AcmVmPSIjcG9pbnRlcnMiLz4NCiAgICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNjAsNDApIiBj%0D%0AbGlwLXBhdGg9InVybCgjY2xpcF9wb2ludCkiPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFw%0D%0AaF9mIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMjAsMCkiLz4NCiAgICAgPHVzZSB4bGluazpocmVm%0D%0APSIjZ3JhcGhfZiIgc3Ryb2tlLW9wYWNpdHk9IjAuNSIvPg0KICAgIDwvZz4NCiAgICA8ZyB0cmFu%0D%0Ac2Zvcm09InRyYW5zbGF0ZSgtNDUsNzApIiBjbGlwLXBhdGg9InVybCgjY2xpcF9wb2ludCkiPg0K%0D%0AICAgICA8ZyBjbGlwLXBhdGg9InVybCgjY2xpcF9ncmFwaF9mKSI+PHVzZSB4bGluazpocmVmPSIj%0D%0AZ3JhcGhfZiIgY2xhc3M9InBvaW50XzEiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMCwwKSIvPjwv%0D%0AZz4NCiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUo%0D%0ALTEwLDApIi8+DQogICAgIDx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2YiIHN0cm9rZS1vcGFjaXR5%0D%0APSIwLjUiLz4NCiAgICA8L2c+DQogICAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCwxMDApIiBj%0D%0AbGlwLXBhdGg9InVybCgjY2xpcF9wb2ludCkiPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFw%0D%0AaF9mIiBjbGFzcz0icG9pbnRfMiIvPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFwaF9mIiBz%0D%0AdHJva2Utb3BhY2l0eT0iMC41Ii8+DQogICAgPC9nPg0KICAgIDxnIHRyYW5zZm9ybT0idHJhbnNs%0D%0AYXRlKDQ1LDcwKSIgY2xpcC1wYXRoPSJ1cmwoI2NsaXBfcG9pbnQpIj4NCiAgICAgPGcgY2xpcC1w%0D%0AYXRoPSJ1cmwoI2NsaXBfZ3JhcGhfZikiPjx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2YiIGNsYXNz%0D%0APSJwb2ludF8zIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxMCwwKSIvPjwvZz4NCiAgICAgPHVzZSB4%0D%0AbGluazpocmVmPSIjZ3JhcGhfZiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMTAsMCkiLz4NCiAgICAg%0D%0APHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZiIgc3Ryb2tlLW9wYWNpdHk9IjAuNSIvPg0KICAgIDwv%0D%0AZz4NCiAgICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSg2MCw0MCkiIGNsaXAtcGF0aD0idXJsKCNj%0D%0AbGlwX3BvaW50KSI+DQogICAgIDx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2YiIHRyYW5zZm9ybT0i%0D%0AdHJhbnNsYXRlKDIwLDApIi8+DQogICAgIDx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2YiIHN0cm9r%0D%0AZS1vcGFjaXR5PSIwLjUiLz4NCiAgICA8L2c+DQogICA8L2c+DQogICA8ZyB0cmFuc2Zvcm09InRy%0D%0AYW5zbGF0ZSgwLDM1MCkiPg0KICAgIDx0ZXh0IHg9Ii02NSIgeT0iLTIwIj5nJiM4OTAyO2c8L3Rl%0D%0AeHQ+PHVzZSB4bGluazpocmVmPSIjZ3JhcGhfYmlnX2dnIi8+DQogICAgPHVzZSB4bGluazpocmVm%0D%0APSIjYXJyb3dfMSIgY2xhc3M9InBvaW50XzEiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0yMCwwKSIv%0D%0APg0KICAgIDx1c2UgeGxpbms6aHJlZj0iI2Fycm93XzQiIGNsYXNzPSJwb2ludF8yIiB0cmFuc2Zv%0D%0Acm09InRyYW5zbGF0ZSggIDAsMCkiLz4NCiAgICA8dXNlIHhsaW5rOmhyZWY9IiNhcnJvd18xIiBj%0D%0AbGFzcz0icG9pbnRfMyIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoIDIwLDApIi8+DQogICAgPHVzZSB4%0D%0AbGluazpocmVmPSIjcG9pbnRlcnMiLz4NCiAgICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNjAs%0D%0ANDApIiBjbGlwLXBhdGg9InVybCgjY2xpcF9wb2ludCkiPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9%0D%0AIiNncmFwaF9nIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMjAsMCkiLz4NCiAgICAgPHVzZSB4bGlu%0D%0AazpocmVmPSIjZ3JhcGhfZyIgc3Ryb2tlLW9wYWNpdHk9IjAuNSIvPg0KICAgIDwvZz4NCiAgICA8%0D%0AZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNDUsNzApIiBjbGlwLXBhdGg9InVybCgjY2xpcF9wb2lu%0D%0AdCkiPg0KICAgICA8ZyBjbGlwLXBhdGg9InVybCgjY2xpcF9ncmFwaF9nKSI+PHVzZSB4bGluazpo%0D%0AcmVmPSIjZ3JhcGhfZyIgY2xhc3M9InBvaW50XzEiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMCww%0D%0AKSIvPjwvZz4NCiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZyIgdHJhbnNmb3JtPSJ0cmFu%0D%0Ac2xhdGUoLTEwLDApIi8+DQogICAgIDx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2ciIHN0cm9rZS1v%0D%0AcGFjaXR5PSIwLjUiLz4NCiAgICA8L2c+DQogICAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCwx%0D%0AMDApIiBjbGlwLXBhdGg9InVybCgjY2xpcF9wb2ludCkiPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9%0D%0AIiNncmFwaF9nIiBjbGFzcz0icG9pbnRfMiIvPg0KICAgICA8dXNlIHhsaW5rOmhyZWY9IiNncmFw%0D%0AaF9nIiBzdHJva2Utb3BhY2l0eT0iMC41Ii8+DQogICAgPC9nPg0KICAgIDxnIHRyYW5zZm9ybT0i%0D%0AdHJhbnNsYXRlKDQ1LDcwKSIgY2xpcC1wYXRoPSJ1cmwoI2NsaXBfcG9pbnQpIj4NCiAgICAgPGcg%0D%0AY2xpcC1wYXRoPSJ1cmwoI2NsaXBfZ3JhcGhfZykiPjx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2ci%0D%0AIGNsYXNzPSJwb2ludF8zIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxMCwwKSIvPjwvZz4NCiAgICAg%0D%0APHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZyIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMTAsMCkiLz4N%0D%0ACiAgICAgPHVzZSB4bGluazpocmVmPSIjZ3JhcGhfZyIgc3Ryb2tlLW9wYWNpdHk9IjAuNSIvPg0K%0D%0AICAgIDwvZz4NCiAgICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSg2MCw0MCkiIGNsaXAtcGF0aD0i%0D%0AdXJsKCNjbGlwX3BvaW50KSI+DQogICAgIDx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2ciIHRyYW5z%0D%0AZm9ybT0idHJhbnNsYXRlKDIwLDApIi8+DQogICAgIDx1c2UgeGxpbms6aHJlZj0iI2dyYXBoX2ci%0D%0AIHN0cm9rZS1vcGFjaXR5PSIwLjUiLz4NCiAgICA8L2c+DQogICA8L2c+DQogIDwvZz4NCiA8L2c+%0D%0ADQo8L3N2Zz4NCg==)
