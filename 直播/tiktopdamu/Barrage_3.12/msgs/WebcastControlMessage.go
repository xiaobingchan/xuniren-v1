package msgs
type WebcastControlMessage struct {
	FloatStyle float64 `json:"floatStyle"`
	Streamer string `json:"streamer"`
	Common struct {
		Monitor float64 `json:"monitor"`
		AnchorFoldType string `json:"anchorFoldType"`
		MsgProcessFilterV string `json:"msgProcessFilterV"`
		AnchorPriorityScore string `json:"anchorPriorityScore"`
		Method string `json:"method"`
		MsgId string `json:"msgId"`
		Describe string `json:"describe"`
		PriorityScore string `json:"priorityScore"`
		ToIdc string `json:"toIdc"`
		FoldTypeForWeb string `json:"foldTypeForWeb"`
		RoomId string `json:"roomId"`
		FoldType string `json:"foldType"`
		FromIdc string `json:"fromIdc"`
		AnchorFoldTypeForWeb string `json:"anchorFoldTypeForWeb"`
		ClientSendTime string `json:"clientSendTime"`
		DispatchStrategy float64 `json:"dispatchStrategy"`
		CreateTime string `json:"createTime"`
		IsShowMsg bool `json:"isShowMsg"`
		LogId string `json:"logId"`
		MsgProcessFilterK string `json:"msgProcessFilterK"`
		RoomMessageHeatLevel string `json:"roomMessageHeatLevel"`
	} `json:"common"`
	Action string `json:"action"`
	Tips string `json:"tips"`
	Extra struct {
		ReasonNo string `json:"reasonNo"`
		Source string `json:"source"`
		BanInfoUrl string `json:"banInfoUrl"`
	} `json:"extra"`
}
