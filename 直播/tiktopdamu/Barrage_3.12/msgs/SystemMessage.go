package msgs
type SystemMessage struct {
	IsWelcome bool `json:"isWelcome"`
	Streamer string `json:"streamer"`
	Common struct {
		AnchorFoldType string `json:"anchorFoldType"`
		PriorityScore string `json:"priorityScore"`
		MsgProcessFilterV string `json:"msgProcessFilterV"`
		FromIdc string `json:"fromIdc"`
		RoomMessageHeatLevel string `json:"roomMessageHeatLevel"`
		AnchorFoldTypeForWeb string `json:"anchorFoldTypeForWeb"`
		MsgId string `json:"msgId"`
		IsShowMsg bool `json:"isShowMsg"`
		ToIdc string `json:"toIdc"`
		Method string `json:"method"`
		MsgProcessFilterK string `json:"msgProcessFilterK"`
		AnchorPriorityScore string `json:"anchorPriorityScore"`
		ClientSendTime string `json:"clientSendTime"`
		RoomId string `json:"roomId"`
		Monitor float64 `json:"monitor"`
		Describe string `json:"describe"`
		FoldType string `json:"foldType"`
		LogId string `json:"logId"`
		FoldTypeForWeb string `json:"foldTypeForWeb"`
		DispatchStrategy float64 `json:"dispatchStrategy"`
		CreateTime string `json:"createTime"`
	} `json:"common"`
	Content string `json:"content"`
	SupprotLandscape bool `json:"supprotLandscape"`
	Source string `json:"source"`
	Scene string `json:"scene"`
}
