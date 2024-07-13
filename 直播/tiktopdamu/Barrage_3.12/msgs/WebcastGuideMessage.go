package msgs
type WebcastGuideMessage struct {
	GuideType string `json:"guideType"`
	GiftId string `json:"giftId"`
	Description string `json:"description"`
	Duration string `json:"duration"`
	DisplayStyle string `json:"displayStyle"`
	Scene string `json:"scene"`
	Streamer string `json:"streamer"`
	Common struct {
		AnchorPriorityScore string `json:"anchorPriorityScore"`
		ClientSendTime string `json:"clientSendTime"`
		RoomId string `json:"roomId"`
		CreateTime string `json:"createTime"`
		Describe string `json:"describe"`
		FoldType string `json:"foldType"`
		ToIdc string `json:"toIdc"`
		Method string `json:"method"`
		Monitor float64 `json:"monitor"`
		IsShowMsg bool `json:"isShowMsg"`
		PriorityScore string `json:"priorityScore"`
		LogId string `json:"logId"`
		MsgId string `json:"msgId"`
		AnchorFoldType string `json:"anchorFoldType"`
		MsgProcessFilterK string `json:"msgProcessFilterK"`
		FromIdc string `json:"fromIdc"`
		RoomMessageHeatLevel string `json:"roomMessageHeatLevel"`
		MsgProcessFilterV string `json:"msgProcessFilterV"`
		FoldTypeForWeb string `json:"foldTypeForWeb"`
		AnchorFoldTypeForWeb string `json:"anchorFoldTypeForWeb"`
		DispatchStrategy float64 `json:"dispatchStrategy"`
	} `json:"common"`
}
