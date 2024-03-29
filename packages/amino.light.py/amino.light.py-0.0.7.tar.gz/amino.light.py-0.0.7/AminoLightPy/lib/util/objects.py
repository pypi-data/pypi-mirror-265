# You don't even know how long this shit took...
# F*ck you Sand for making me do this.

class Objects:
    class Users:
        team_amino = "000000000-0000-0000-0000-000000000000"
        news_feed = "000000000-0000-0000-0000-000000000001"

class UserProfile:
    __slots__ = (
        "json", "fanClub", "accountMembershipStatus", "activation", "activePublicLiveThreadId",
        "age", "aminoId", "aminoIdEditable", "appleId", "avatarFrame", "avatarFrameId",
        "blogsCount", "commentsCount", "content", "dateOfBirth", "createdTime", "email",
        "facebookId", "followersCount", "followingCount", "followingStatus", "gender",
        "googleId", "icon", "isGlobal", "isNicknameVerified", "itemsCount", "level",
        "mediaList", "membershipStatus", "modifiedTime", "mood", "moodSticker", "nickname",
        "notificationSubscriptionStatus", "onlineStatus", "onlineStatus2", "phoneNumber",
        "postsCount", "pushEnabled", "race", "reputation", "role", "securityLevel",
        "status", "storiesCount", "tagList", "twitterId", "userId", "verified",
        "totalQuizHighestScore", "totalQuizPlayedTimes", "requestId", "message", "applicant",
        "avgDailySpendTimeIn7Days", "adminLogCountIn7Days", "extensions", "style",
        "backgroundImage", "backgroundColor", "coverAnimation", "customTitles", "defaultBubbleId",
        "disabledLevel", "disabledStatus", "disabledTime", "isMemberOfTeamAmino",
        "privilegeOfChatInviteRequest", "privilegeOfCommentOnUserProfile", "influencerInfo",
        "fansCount", "influencerCreatedTime", "influencerMonthlyFee", "influencerPinned",
        "staffInfo", "globalStrikeCount", "lastStrikeTime", "lastWarningTime", "strikeCount",
        "warningCount", "session"
    )

    def __init__(self, data: dict):
        if not data:
            return

        self.json = data

        self.fanClub = FanClubList(data.get("fanClubList", [])).FanClubList if data else None

        self.accountMembershipStatus = data.get("accountMembershipStatus")
        self.activation = data.get("activation")
        self.activePublicLiveThreadId = data.get("activePublicLiveThreadId")
        self.age = data.get("age")
        self.aminoId = data.get("aminoId")
        self.aminoIdEditable = data.get("aminoIdEditable")
        self.appleId = data.get("appleID")
        self.avatarFrame = data.get("avatarFrame")
        self.avatarFrameId = data.get("avatarFrameId")
        self.blogsCount = data.get("blogsCount")
        self.commentsCount = data.get("commentsCount")
        self.content = data.get("content")
        self.dateOfBirth = data.get("dateOfBirth")
        self.createdTime = data.get("createdTime")
        self.email = data.get("email")
        self.facebookId = data.get("facebookID")
        self.followersCount = data.get("membersCount")
        self.followingCount = data.get("joinedCount")
        self.followingStatus = data.get("followingStatus")
        self.gender = data.get("gender")
        self.googleId = data.get("googleID")
        self.icon = data.get("icon")
        self.isGlobal = data.get("isGlobal")
        self.isNicknameVerified = data.get("isNicknameVerified")
        self.itemsCount = data.get("itemsCount")
        self.level = data.get("level")
        self.mediaList = data.get("mediaList")
        self.membershipStatus = data.get("membershipStatus")
        self.modifiedTime = data.get("modifiedTime")
        self.mood = data.get("mood")
        self.moodSticker = data.get("moodSticker")
        self.nickname = data.get("nickname")
        self.notificationSubscriptionStatus = data.get("notificationSubscriptionStatus")
        self.onlineStatus = data.get("onlineStatus")
        self.onlineStatus2 = data.get("settings", {}).get("onlineStatus")
        self.phoneNumber = data.get("phoneNumber")
        self.postsCount = data.get("postsCount")
        self.pushEnabled = data.get("pushEnabled")
        self.race = data.get("race")
        self.reputation = data.get("reputation")
        self.role = data.get("role")
        self.securityLevel = data.get("securityLevel")
        self.status = data.get("status")
        self.storiesCount = data.get("storiesCount")
        self.tagList = data.get("tagList")
        self.twitterId = data.get("twitterID")
        self.userId = data.get("uid")
        self.verified = data.get("verified")
        self.totalQuizHighestScore = data.get("totalQuizHighestScore")
        self.totalQuizPlayedTimes = data.get("totalQuizPlayedTimes")
        self.requestId = data.get("requestId")
        self.message = data.get("message")
        self.applicant = data.get("applicant")
        self.avgDailySpendTimeIn7Days = data.get("avgDailySpendTimeIn7Days")
        self.adminLogCountIn7Days = data.get("adminLogCountIn7Days")

        #extensions
        self.extensions = data.get("extensions", {"style": {}})
        #style
        self.style = self.extensions.get("style", {}) if self.extensions else {}
        self.backgroundImage = self.style.get("backgroundImage") 
        self.backgroundColor = self.style.get("backgroundColor")

        self.coverAnimation = self.extensions.get("coverAnimation") if self.extensions else None
        self.customTitles = self.extensions.get("customTitles") if self.extensions else None
        self.defaultBubbleId = self.extensions.get("defaultBubbleId") if self.extensions else None
        self.disabledLevel = self.extensions.get("__disabledLevel__") if self.extensions else None
        self.disabledStatus = self.extensions.get("__disabledStatus__") if self.extensions else None
        self.disabledTime = self.extensions.get("__disabledTime__") if self.extensions else None
        self.isMemberOfTeamAmino = self.extensions.get("isMemberOfTeamAmino") if self.extensions else None
        self.privilegeOfChatInviteRequest = self.extensions.get("privilegeOfChatInviteRequest") if self.extensions else None
        self.privilegeOfCommentOnUserProfile = self.extensions.get("privilegeOfCommentOnUserProfile") if self.extensions else None
        
        
        #influencerInfo
        self.influencerInfo = data.get("influencerInfo", {})
        self.fansCount = self.influencerInfo.get("fansCount") if self.influencerInfo else None
        self.influencerCreatedTime = self.influencerInfo.get("createdTime") if self.influencerInfo else None
        self.influencerMonthlyFee = data.get("monthlyFee") if self.influencerInfo else None
        self.influencerPinned = data.get("pinned") if self.influencerInfo else None


        #adminInfo
        self.staffInfo = data.get("adminInfo", {})
        self.globalStrikeCount = self.staffInfo.get("globalStrikeCount") if self.staffInfo else None
        self.lastStrikeTime = self.staffInfo.get("lastStrikeTime") if self.staffInfo else None
        self.lastWarningTime = self.staffInfo.get("lastWarningTime") if self.staffInfo else None
        self.strikeCount = self.staffInfo.get("strikeCount") if self.staffInfo else None
        self.warningCount = self.staffInfo.get("warningCount") if self.staffInfo else None

        
        self.session = None

    @property
    def UserProfile(self):

        return self

class UserProfileList:
    __slots__ = (
        "json", "fanClub", "accountMembershipStatus", "activation", "activePublicLiveThreadId",
        "age", "aminoId", "aminoIdEditable", "appleId", "avatarFrame", "avatarFrameId",
        "blogsCount", "commentsCount", "content", "dateOfBirth", "createdTime", "email",
        "facebookId", "followersCount", "followingCount", "followingStatus", "gender",
        "googleId", "icon", "isGlobal", "isNicknameVerified", "itemsCount", "level",
        "mediaList", "membershipStatus", "modifiedTime", "mood", "moodSticker", "nickname",
        "notificationSubscriptionStatus", "onlineStatus", "onlineStatus2", "phoneNumber",
        "postsCount", "pushEnabled", "race", "reputation", "role", "securityLevel",
        "status", "storiesCount", "tagList", "twitterId", "userId", "verified",
        "totalQuizHighestScore", "totalQuizPlayedTimes", "requestId", "message", "applicant",
        "avgDailySpendTimeIn7Days", "adminLogCountIn7Days", "extensions", "style",
        "backgroundImage", "backgroundColor", "coverAnimation", "customTitles", "defaultBubbleId",
        "disabledLevel", "disabledStatus", "disabledTime", "isMemberOfTeamAmino",
        "privilegeOfChatInviteRequest", "privilegeOfCommentOnUserProfile", "influencerInfo",
        "fansCount", "influencerCreatedTime", "influencerMonthlyFee", "influencerPinned",
        "staffInfo", "globalStrikeCount", "lastStrikeTime", "lastWarningTime", "strikeCount",
        "warningCount", "session"
    )

    def __init__(self, data):
        self.json = data
        _userObjects = tuple(UserProfile(x).UserProfile for x in data)

        if _userObjects:
            attributes = tuple(attr for attr in dir(_userObjects[0]) if not attr.startswith('__') and not callable(getattr(_userObjects[0], attr)) and attr != _userObjects[0].__class__.__name__)
            for attr in attributes:
                setattr(self, attr, tuple(getattr(user, attr, None) for user in _userObjects))

    @property
    def UserProfileList(self):
        return self

class BlogList:
    def __init__(self, data, nextPageToken = None, prevPageToken = None):
        _author, _quizQuestionList = [], []

        self.json = data
        self.nextPageToken = nextPageToken
        self.prevPageToken = prevPageToken

        for y in data:
            try: _author.append(y["author"])
            except (KeyError, TypeError): _author.append(None)
            try: _quizQuestionList.append(QuizQuestionList(y["quizQuestionList"]).QuizQuestionList)
            except (KeyError, TypeError): _quizQuestionList.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.quizQuestionList = _quizQuestionList

        self.createdTime = []
        self.globalVotesCount = []
        self.globalVotedValue = []
        self.keywords = []
        self.mediaList = []
        self.style = []
        self.totalQuizPlayCount = []
        self.title = []
        self.tipInfo = []
        self.tippersCount = []
        self.tippable = []
        self.tippedCoins = []
        self.contentRating = []
        self.needHidden = []
        self.guestVotesCount = []
        self.type = []
        self.status = []
        self.globalCommentsCount = []
        self.modifiedTime = []
        self.widgetDisplayInterval = []
        self.totalPollVoteCount = []
        self.blogId = []
        self.viewCount = []
        self.fansOnly = []
        self.backgroundColor = []
        self.votesCount = []
        self.endTime = []
        self.refObjectId = []
        self.refObject = []
        self.votedValue = []
        self.extensions = []
        self.commentsCount = []
        self.content = []
        self.featuredType = []
        self.shareUrl = []
        self.disabledTime = []
        self.quizPlayedTimes = []
        self.quizTotalQuestionCount = []
        self.quizTrendingTimes = []
        self.quizLastAddQuestionTime = []
        self.isIntroPost = []

    @property
    def BlogList(self):
        for x in self.json:
            try: self.globalVotesCount.append(x["globalVotesCount"])
            except (KeyError, TypeError): self.globalVotesCount.append(None)
            try: self.globalVotedValue.append(x["globalVotedValue"])
            except (KeyError, TypeError): self.globalVotedValue.append(None)
            try: self.keywords.append(x["keywords"])
            except (KeyError, TypeError): self.keywords.append(None)
            try: self.mediaList.append(x["mediaList"])
            except (KeyError, TypeError): self.mediaList.append(None)
            try: self.style.append(x["style"])
            except (KeyError, TypeError): self.style.append(None)
            try: self.totalQuizPlayCount.append(x["totalQuizPlayCount"])
            except (KeyError, TypeError): self.totalQuizPlayCount.append(None)
            try: self.title.append(x["title"])
            except (KeyError, TypeError): self.title.append(None)
            try: self.tipInfo.append(x["tipInfo"])
            except (KeyError, TypeError): self.tipInfo.append(None)
            try: self.tippersCount.append(x["tipInfo"]["tippersCount"])
            except (KeyError, TypeError): self.tippersCount.append(None)
            try: self.tippable.append(x["tipInfo"]["tippable"])
            except (KeyError, TypeError): self.tippable.append(None)
            try: self.tippedCoins.append(x["tipInfo"]["tippedCoins"])
            except (KeyError, TypeError): self.tippedCoins.append(None)
            try: self.contentRating.append(x["contentRating"])
            except (KeyError, TypeError): self.contentRating.append(None)
            try: self.needHidden.append(x["needHidden"])
            except (KeyError, TypeError): self.needHidden.append(None)
            try: self.guestVotesCount.append(x["guestVotesCount"])
            except (KeyError, TypeError): self.guestVotesCount.append(None)
            try: self.type.append(x["type"])
            except (KeyError, TypeError): self.type.append(None)
            try: self.status.append(x["status"])
            except (KeyError, TypeError): self.status.append(None)
            try: self.globalCommentsCount.append(x["globalCommentsCount"])
            except (KeyError, TypeError): self.globalCommentsCount.append(None)
            try: self.modifiedTime.append(x["modifiedTime"])
            except (KeyError, TypeError): self.modifiedTime.append(None)
            try: self.widgetDisplayInterval.append(x["widgetDisplayInterval"])
            except (KeyError, TypeError): self.widgetDisplayInterval.append(None)
            try: self.totalPollVoteCount.append(x["totalPollVoteCount"])
            except (KeyError, TypeError): self.totalPollVoteCount.append(None)
            try: self.blogId.append(x["blogId"])
            except (KeyError, TypeError): self.blogId.append(None)
            try: self.viewCount.append(x["viewCount"])
            except (KeyError, TypeError): self.viewCount.append(None)
            try: self.fansOnly.append(x["extensions"]["fansOnly"])
            except (KeyError, TypeError): self.fansOnly.append(None)
            try: self.backgroundColor.append(x["extensions"]["style"]["backgroundColor"])
            except (KeyError, TypeError): self.backgroundColor.append(None)
            try: self.votesCount.append(x["votesCount"])
            except (KeyError, TypeError): self.votesCount.append(None)
            try: self.endTime.append(x["endTime"])
            except (KeyError, TypeError): self.endTime.append(None)
            try: self.refObjectId.append(x["refObjectId"])
            except (KeyError, TypeError): self.refObjectId.append(None)
            try: self.refObject.append(x["refObject"])
            except (KeyError, TypeError): self.refObject.append(None)
            try: self.votedValue.append(x["votedValue"])
            except (KeyError, TypeError): self.votedValue.append(None)
            try: self.content.append(x["content"])
            except (KeyError, TypeError): self.content.append(None)
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)
            try: self.extensions.append(x["extensions"])
            except (KeyError, TypeError): self.extensions.append(None)
            try: self.shareUrl.append(x["shareURLFullPath"])
            except (KeyError, TypeError): self.shareUrl.append(None)
            try: self.commentsCount.append(x["commentsCount"])
            except (KeyError, TypeError): self.commentsCount.append(None)
            try: self.featuredType.append(x["extensions"]["featuredType"])
            except (KeyError, TypeError): self.featuredType.append(None)
            try: self.disabledTime.append(x["extensions"]["__disabledTime__"])
            except (KeyError, TypeError): self.disabledTime.append(None)
            try: self.quizPlayedTimes.append(x["extensions"]["quizPlayedTimes"])
            except (KeyError, TypeError): self.quizPlayedTimes.append(None)
            try: self.quizTotalQuestionCount.append(x["extensions"]["quizTotalQuestionCount"])
            except (KeyError, TypeError): self.quizTotalQuestionCount.append(None)
            try: self.quizTrendingTimes.append(x["extensions"]["quizTrendingTimes"])
            except (KeyError, TypeError): self.quizTrendingTimes.append(None)
            try: self.quizLastAddQuestionTime.append(x["extensions"]["quizLastAddQuestionTime"])
            except (KeyError, TypeError): self.quizLastAddQuestionTime.append(None)
            try: self.isIntroPost.append(x["extensions"]["isIntroPost"])
            except (KeyError, TypeError): self.isIntroPost.append(None)

        return self

class RecentBlogs:
    def __init__(self, data):
        self.json = data

        self.nextPageToken = None
        self.prevPageToken = None

    @property
    def RecentBlogs(self):
        try: self.nextPageToken = self.json["paging"]["nextPageToken"]
        except (KeyError, TypeError): pass
        try: self.prevPageToken = self.json["paging"]["prevPageToken"]
        except (KeyError, TypeError): pass

        return BlogList(self.json["blogList"], self.nextPageToken, self.prevPageToken).BlogList

class BlogCategoryList:
    def __init__(self, data):
        self.json = data
        self.status = []
        self.modifiedTime = []
        self.icon = []
        self.style = []
        self.title = []
        self.content = []
        self.createdTime = []
        self.position = []
        self.type = []
        self.categoryId = []
        self.blogsCount = []

    @property
    def BlogCategoryList(self):
        for x in self.json:
            try: self.status.append(x["status"])
            except (KeyError, TypeError): self.status.append(None)
            try: self.modifiedTime.append(x["modifiedTime"])
            except (KeyError, TypeError): self.modifiedTime.append(None)
            try: self.icon.append(x["icon"])
            except (KeyError, TypeError): self.icon.append(None)
            try: self.style.append(x["style"])
            except (KeyError, TypeError): self.style.append(None)
            try: self.title.append(x["label"])
            except (KeyError, TypeError): self.title.append(None)
            try: self.content.append(x["content"])
            except (KeyError, TypeError): self.content.append(None)
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)
            try: self.position.append(x["position"])
            except (KeyError, TypeError): self.position.append(None)
            try: self.type.append(x["type"])
            except (KeyError, TypeError): self.type.append(None)
            try: self.categoryId.append(x["categoryId"])
            except (KeyError, TypeError): self.categoryId.append(None)
            try: self.blogsCount.append(x["blogsCount"])
            except (KeyError, TypeError): self.blogsCount.append(None)

        return self

class Blog:
    def __init__(self, data):
        self.json = data

        try: self.author: UserProfile = UserProfile(data["author"]).UserProfile
        except (KeyError, TypeError): self.author: UserProfile = UserProfile([])
        try: self.quizQuestionList: QuizQuestionList = QuizQuestionList(data["quizQuestionList"]).QuizQuestionList
        except (KeyError, TypeError): self.quizQuestionList: QuizQuestionList = QuizQuestionList([])

        self.createdTime = None
        self.globalVotesCount = None
        self.globalVotedValue = None
        self.keywords = None
        self.mediaList = None
        self.style = None
        self.totalQuizPlayCount = None
        self.title = None
        self.tipInfo = None
        self.tippersCount = None
        self.tippable = None
        self.tippedCoins = None
        self.contentRating = None
        self.needHidden = None
        self.guestVotesCount = None
        self.type = None
        self.status = None
        self.globalCommentsCount = None
        self.modifiedTime = None
        self.widgetDisplayInterval = None
        self.totalPollVoteCount = None
        self.blogId = None
        self.comId = None
        self.viewCount = None
        self.fansOnly = None
        self.backgroundColor = None
        self.votesCount = None
        self.endTime = None
        self.refObjectId = None
        self.refObject = None
        self.votedValue = None
        self.extensions = None
        self.commentsCount = None
        self.content = None
        self.featuredType = None
        self.shareUrl = None
        self.disabledTime = None
        self.quizPlayedTimes = None
        self.quizTotalQuestionCount = None
        self.quizTrendingTimes = None
        self.quizLastAddQuestionTime = None
        self.isIntroPost = None

    @property
    def Blog(self):
        try: self.globalVotesCount = self.json["globalVotesCount"]
        except (KeyError, TypeError): pass
        try: self.globalVotedValue = self.json["globalVotedValue"]
        except (KeyError, TypeError): pass
        try: self.keywords = self.json["keywords"]
        except (KeyError, TypeError): pass
        try: self.mediaList = self.json["mediaList"]
        except (KeyError, TypeError): pass
        try: self.style = self.json["style"]
        except (KeyError, TypeError): pass
        try: self.totalQuizPlayCount = self.json["totalQuizPlayCount"]
        except (KeyError, TypeError): pass
        try: self.title = self.json["title"]
        except (KeyError, TypeError): pass
        try: self.tipInfo = self.json["tipInfo"]
        except (KeyError, TypeError): pass
        try: self.tippersCount = self.json["tipInfo"]["tippersCount"]
        except (KeyError, TypeError): pass
        try: self.tippable = self.json["tipInfo"]["tippable"]
        except (KeyError, TypeError): pass
        try: self.tippedCoins = self.json["tipInfo"]["tippedCoins"]
        except (KeyError, TypeError): pass
        try: self.contentRating = self.json["contentRating"]
        except (KeyError, TypeError): pass
        try: self.needHidden = self.json["needHidden"]
        except (KeyError, TypeError): pass
        try: self.guestVotesCount = self.json["guestVotesCount"]
        except (KeyError, TypeError): pass
        try: self.type = self.json["type"]
        except (KeyError, TypeError): pass
        try: self.status = self.json["status"]
        except (KeyError, TypeError): pass
        try: self.globalCommentsCount = self.json["globalCommentsCount"]
        except (KeyError, TypeError): pass
        try: self.modifiedTime = self.json["modifiedTime"]
        except (KeyError, TypeError): pass
        try: self.widgetDisplayInterval = self.json["widgetDisplayInterval"]
        except (KeyError, TypeError): pass
        try: self.totalPollVoteCount = self.json["totalPollVoteCount"]
        except (KeyError, TypeError): pass
        try: self.blogId = self.json["blogId"]
        except (KeyError, TypeError): pass
        try: self.comId = self.json["ndcId"]
        except (KeyError, TypeError): pass
        try: self.viewCount = self.json["viewCount"]
        except (KeyError, TypeError): pass
        try: self.shareUrl = self.json["shareURLFullPath"]
        except (KeyError, TypeError): pass
        try: self.fansOnly = self.json["extensions"]["fansOnly"]
        except (KeyError, TypeError): pass
        try: self.backgroundColor = self.json["extensions"]["style"]["backgroundColor"]
        except (KeyError, TypeError): pass
        try: self.votesCount = self.json["votesCount"]
        except (KeyError, TypeError): pass
        try: self.endTime = self.json["endTime"]
        except (KeyError, TypeError): pass
        try: self.refObjectId = self.json["refObjectId"]
        except (KeyError, TypeError): pass
        try: self.refObject = self.json["refObject"]
        except (KeyError, TypeError): pass
        try: self.votedValue = self.json["votedValue"]
        except (KeyError, TypeError): pass
        try: self.content = self.json["content"]
        except (KeyError, TypeError): pass
        try: self.createdTime = self.json["createdTime"]
        except (KeyError, TypeError): pass
        try: self.extensions = self.json["extensions"]
        except (KeyError, TypeError): pass
        try: self.commentsCount = self.json["commentsCount"]
        except (KeyError, TypeError): pass
        try: self.featuredType = self.json["extensions"]["featuredType"]
        except (KeyError, TypeError): pass
        try: self.disabledTime = self.json["extensions"]["__disabledTime__"]
        except (KeyError, TypeError): pass
        try: self.quizPlayedTimes = self.json["extensions"]["quizPlayedTimes"]
        except (KeyError, TypeError): pass
        try: self.quizTotalQuestionCount = self.json["extensions"]["quizTotalQuestionCount"]
        except (KeyError, TypeError): pass
        try: self.quizTrendingTimes = self.json["extensions"]["quizTrendingTimes"]
        except (KeyError, TypeError): pass
        try: self.quizLastAddQuestionTime = self.json["extensions"]["quizLastAddQuestionTime"]
        except (KeyError, TypeError): pass
        try: self.isIntroPost = self.json["extensions"]["isIntroPost"]
        except (KeyError, TypeError): pass

        return self

class Wiki:
    def __init__(self, data):
        self.json = data

        try: self.author: UserProfile = UserProfile(data["author"]).UserProfile
        except (KeyError, TypeError): self.author: UserProfile = UserProfile([])
        try: self.labels: WikiLabelList = WikiLabelList(data["extensions"]["props"]).WikiLabelList
        except (KeyError, TypeError): self.labels: WikiLabelList = WikiLabelList([])

        self.createdTime = None
        self.modifiedTime = None
        self.wikiId = None
        self.status = None
        self.style = None
        self.globalCommentsCount = None
        self.votedValue = None
        self.globalVotesCount = None
        self.globalVotedValue = None
        self.contentRating = None
        self.title = None
        self.content = None
        self.keywords = None
        self.needHidden = None
        self.guestVotesCount = None
        self.extensions = None
        self.backgroundColor = None
        self.fansOnly = None
        self.knowledgeBase = None
        self.originalWikiId = None
        self.version = None
        self.contributors = None
        self.votesCount = None
        self.comId = None
        self.createdTime = None
        self.mediaList = None
        self.commentsCount = None

    @property
    def Wiki(self):
        try: self.wikiId = self.json["itemId"]
        except (KeyError, TypeError): pass
        try: self.status = self.json["status"]
        except (KeyError, TypeError): pass
        try: self.style = self.json["style"]
        except (KeyError, TypeError): pass
        try: self.globalCommentsCount = self.json["globalCommentsCount"]
        except (KeyError, TypeError): pass
        try: self.modifiedTime = self.json["modifiedTime"]
        except (KeyError, TypeError): pass
        try: self.votedValue = self.json["votedValue"]
        except (KeyError, TypeError): pass
        try: self.globalVotesCount = self.json["globalVotesCount"]
        except (KeyError, TypeError): pass
        try: self.globalVotedValue = self.json["globalVotedValue"]
        except (KeyError, TypeError): pass
        try: self.contentRating = self.json["contentRating"]
        except (KeyError, TypeError): pass
        try: self.contentRating = self.json["contentRating"]
        except (KeyError, TypeError): pass
        try: self.title = self.json["label"]
        except (KeyError, TypeError): pass
        try: self.content = self.json["content"]
        except (KeyError, TypeError): pass
        try: self.keywords = self.json["keywords"]
        except (KeyError, TypeError): pass
        try: self.needHidden = self.json["needHidden"]
        except (KeyError, TypeError): pass
        try: self.guestVotesCount = self.json["guestVotesCount"]
        except (KeyError, TypeError): pass
        try: self.extensions = self.json["extensions"]
        except (KeyError, TypeError): pass
        try: self.votesCount = self.json["votesCount"]
        except (KeyError, TypeError): pass
        try: self.comId = self.json["ndcId"]
        except (KeyError, TypeError): pass
        try: self.createdTime = self.json["createdTime"]
        except (KeyError, TypeError): pass
        try: self.mediaList = self.json["mediaList"]
        except (KeyError, TypeError): pass
        try: self.commentsCount = self.json["commentsCount"]
        except (KeyError, TypeError): pass
        try: self.backgroundColor = self.json["extensions"]["style"]["backgroundColor"]
        except (KeyError, TypeError): pass
        try: self.fansOnly = self.json["extensions"]["fansOnly"]
        except (KeyError, TypeError): pass
        try: self.knowledgeBase = self.json["extensions"]["knowledgeBase"]
        except (KeyError, TypeError): pass
        try: self.version = self.json["extensions"]["knowledgeBase"]["version"]
        except (KeyError, TypeError): pass
        try: self.originalWikiId = self.json["extensions"]["knowledgeBase"]["originalItemId"]
        except (KeyError, TypeError): pass
        try: self.contributors = self.json["extensions"]["knowledgeBase"]["contributors"]
        except (KeyError, TypeError): pass

        return self

class WikiList:
    def __init__(self, data: dict):
        self.json = data

        self.author = UserProfileList([y.get("author") for y in data]).UserProfileList
        self.labels = tuple(WikiLabelList(y["extensions"]["props"]).WikiLabelList if "extensions" in y and "props" in y["extensions"] else None for y in data)

        _wikiObjects = tuple(Wiki(x).Wiki for x in data)

        if _wikiObjects:
            attributes = tuple(attr for attr in dir(_wikiObjects[0]) if not attr.startswith('__') and not callable(getattr(_wikiObjects[0], attr)) and attr != _wikiObjects[0].__class__.__name__)
            for attr in attributes:
                setattr(self, attr, tuple(getattr(user, attr, None) for user in _wikiObjects))

    @property
    def WikiList(self):

        return self


class WikiLabelList:
    def __init__(self, data: dict):
        self.json = data
        self.title = data.get("title")
        self.content = data.get("value")
        self.type = data.get("type")

    @property
    def WikiLabelList(self):

        return self

class RankingTableList:
    def __init__(self, data: dict):
        self.json = data
        self.title = tuple(x.get("title") for x in data)
        self.level = tuple(x.get("level") for x in data)
        self.reputation = tuple(x.get("reputation") for x in data)
        self.id = tuple(x.get("id") for x in data)

    @property
    def RankingTableList(self):

        return self

class Community:
    __slots__ = (
        "json", "agent", "rankingTable", "usersCount", "createdTime", "aminoId",
        "icon", "link", "comId", "modifiedTime", "status", "joinType", "tagline",
        "primaryLanguage", "heat", "themePack", "probationStatus", "listedStatus",
        "userAddedTopicList", "name", "isStandaloneAppDeprecated", "searchable",
        "influencerList", "keywords", "mediaList", "description",
        "isStandaloneAppMonetizationEnabled", "advancedSettings", "activeInfo",
        "configuration", "extensions", "nameAliases", "templateId",
        "promotionalMediaList", "defaultRankingTypeInLeaderboard",
        "joinedBaselineCollectionIdList", "newsfeedPages", "catalogEnabled",
        "pollMinFullBarVoteCount", "leaderboardStyle", "facebookAppIdList",
        "welcomeMessage", "welcomeMessageEnabled", "hasPendingReviewRequest",
        "frontPageLayout", "themeColor", "themeHash", "themeVersion", "themeUrl",
        "themeHomePageAppearance", "themeLeftSidePanelTop", "themeLeftSidePanelBottom",
        "themeLeftSidePanelColor", "customList"
    )

    def __init__(self, data):
        self.json = data

        try: self.agent: UserProfile = UserProfile(data["agent"]).UserProfile
        except (KeyError, TypeError): self.agent: UserProfile = UserProfile([])
        try: self.rankingTable: RankingTableList = RankingTableList(data["advancedSettings"]["rankingTable"]).RankingTableList
        except (KeyError, TypeError): self.rankingTable: RankingTableList = RankingTableList([])

        self.usersCount = None
        self.createdTime = None
        self.aminoId = None
        self.icon = None
        self.link = None
        self.comId = None
        self.modifiedTime = None
        self.status = None
        self.joinType = None
        self.tagline = None
        self.primaryLanguage = None
        self.heat = None
        self.themePack = None
        self.probationStatus = None
        self.listedStatus = None
        self.userAddedTopicList = None
        self.name = None
        self.isStandaloneAppDeprecated = None
        self.searchable = None
        self.influencerList = None
        self.keywords = None
        self.mediaList = None
        self.description = None
        self.isStandaloneAppMonetizationEnabled = None
        self.advancedSettings = None
        self.activeInfo = None
        self.configuration = None
        self.extensions = None
        self.nameAliases = None
        self.templateId = None
        self.promotionalMediaList = None
        self.defaultRankingTypeInLeaderboard = None
        self.joinedBaselineCollectionIdList = None
        self.newsfeedPages = None
        self.catalogEnabled = None
        self.pollMinFullBarVoteCount = None
        self.leaderboardStyle = None
        self.facebookAppIdList = None
        self.welcomeMessage = None
        self.welcomeMessageEnabled = None
        self.hasPendingReviewRequest = None
        self.frontPageLayout = None
        self.themeColor = None
        self.themeHash = None
        self.themeVersion = None
        self.themeUrl = None
        self.themeHomePageAppearance = None
        self.themeLeftSidePanelTop = None
        self.themeLeftSidePanelBottom = None
        self.themeLeftSidePanelColor = None
        self.customList = None

    @property
    def Community(self):
        try: self.name = self.json["name"]
        except (KeyError, TypeError): pass
        try: self.usersCount = self.json["membersCount"]
        except (KeyError, TypeError): pass
        try: self.createdTime = self.json["createdTime"]
        except (KeyError, TypeError): pass
        try: self.aminoId = self.json["endpoint"]
        except (KeyError, TypeError): pass
        try: self.icon = self.json["icon"]
        except (KeyError, TypeError): pass
        try: self.link = self.json["link"]
        except (KeyError, TypeError): pass
        try: self.comId = self.json["ndcId"]
        except (KeyError, TypeError): pass
        try: self.modifiedTime = self.json["modifiedTime"]
        except (KeyError, TypeError): pass
        try: self.status = self.json["status"]
        except (KeyError, TypeError): pass
        try: self.joinType = self.json["joinType"]
        except (KeyError, TypeError): pass
        try: self.primaryLanguage = self.json["primaryLanguage"]
        except (KeyError, TypeError): pass
        try: self.heat = self.json["communityHeat"]
        except (KeyError, TypeError): pass
        try: self.userAddedTopicList = self.json["userAddedTopicList"]
        except (KeyError, TypeError): pass
        try: self.probationStatus = self.json["probationStatus"]
        except (KeyError, TypeError): pass
        try: self.listedStatus = self.json["listedStatus"]
        except (KeyError, TypeError): pass
        try: self.themePack = self.json["themePack"]
        except (KeyError, TypeError): pass
        try: self.themeColor = self.json["themePack"]["themeColor"]
        except (KeyError, TypeError): pass
        try: self.themeHash = self.json["themePack"]["themePackHash"]
        except (KeyError, TypeError): pass
        try: self.themeVersion = self.json["themePack"]["themePackRevision"]
        except (KeyError, TypeError): pass
        try: self.themeUrl = self.json["themePack"]["themePackUrl"]
        except (KeyError, TypeError): pass
        try: self.themeHomePageAppearance = self.json["configuration"]["appearance"]["homePage"]["navigation"]
        except (KeyError, TypeError): pass
        try: self.themeLeftSidePanelTop = self.json["configuration"]["appearance"]["leftSidePanel"]["navigation"]["level1"]
        except (KeyError, TypeError): pass
        try: self.themeLeftSidePanelBottom = self.json["configuration"]["appearance"]["leftSidePanel"]["navigation"]["level2"]
        except (KeyError, TypeError): pass
        try: self.themeLeftSidePanelColor = self.json["configuration"]["appearance"]["leftSidePanel"]["style"]["iconColor"]
        except (KeyError, TypeError): pass
        try: self.customList = self.json["configuration"]["page"]["customList"]
        except (KeyError, TypeError): pass
        try: self.tagline = self.json["tagline"]
        except (KeyError, TypeError): pass
        try: self.searchable = self.json["searchable"]
        except (KeyError, TypeError): pass
        try: self.isStandaloneAppDeprecated = self.json["isStandaloneAppDeprecated"]
        except (KeyError, TypeError): pass
        try: self.influencerList = self.json["influencerList"]
        except (KeyError, TypeError): pass
        try: self.keywords = self.json["keywords"]
        except (KeyError, TypeError): pass
        try: self.mediaList = self.json["mediaList"]
        except (KeyError, TypeError): pass
        try: self.description = self.json["content"]
        except (KeyError, TypeError): pass
        try: self.isStandaloneAppMonetizationEnabled = self.json["isStandaloneAppMonetizationEnabled"]
        except (KeyError, TypeError): pass
        try: self.advancedSettings = self.json["advancedSettings"]
        except (KeyError, TypeError): pass
        try: self.defaultRankingTypeInLeaderboard = self.json["advancedSettings"]["defaultRankingTypeInLeaderboard"]
        except (KeyError, TypeError): pass
        try: self.frontPageLayout = self.json["advancedSettings"]["frontPageLayout"]
        except (KeyError, TypeError): pass
        try: self.hasPendingReviewRequest = self.json["advancedSettings"]["hasPendingReviewRequest"]
        except (KeyError, TypeError): pass
        try: self.welcomeMessageEnabled = self.json["advancedSettings"]["welcomeMessageEnabled"]
        except (KeyError, TypeError): pass
        try: self.welcomeMessage = self.json["advancedSettings"]["welcomeMessageText"]
        except (KeyError, TypeError): pass
        try: self.pollMinFullBarVoteCount = self.json["advancedSettings"]["pollMinFullBarVoteCount"]
        except (KeyError, TypeError): pass
        try: self.catalogEnabled = self.json["advancedSettings"]["catalogEnabled"]
        except (KeyError, TypeError): pass
        try: self.leaderboardStyle = self.json["advancedSettings"]["leaderboardStyle"]
        except (KeyError, TypeError): pass
        try: self.facebookAppIdList = self.json["advancedSettings"]["facebookAppIdList"]
        except (KeyError, TypeError): pass
        try: self.newsfeedPages = self.json["advancedSettings"]["newsfeedPages"]
        except (KeyError, TypeError): pass
        try: self.joinedBaselineCollectionIdList = self.json["advancedSettings"]["joinedBaselineCollectionIdList"]
        except (KeyError, TypeError): pass
        try: self.activeInfo = self.json["activeInfo"]
        except (KeyError, TypeError): pass
        try: self.configuration = self.json["configuration"]
        except (KeyError, TypeError): pass
        try: self.extensions = self.json["extensions"]
        except (KeyError, TypeError): pass
        try: self.nameAliases = self.json["extensions"]["communityNameAliases"]
        except (KeyError, TypeError): pass
        try: self.templateId = self.json["templateId"]
        except (KeyError, TypeError): pass
        try: self.promotionalMediaList = self.json["promotionalMediaList"]
        except (KeyError, TypeError): pass

        return self

class CommunityList:
    __slots__ = (
        "json", "agent", "rankingTable", "usersCount", "createdTime", "aminoId",
        "icon", "link", "comId", "modifiedTime", "status", "joinType", "tagline",
        "primaryLanguage", "heat", "themePack", "probationStatus", "listedStatus",
        "userAddedTopicList", "name", "isStandaloneAppDeprecated", "searchable",
        "influencerList", "keywords", "mediaList", "description",
        "isStandaloneAppMonetizationEnabled", "advancedSettings", "activeInfo",
        "configuration", "extensions", "nameAliases", "templateId",
        "promotionalMediaList", "defaultRankingTypeInLeaderboard",
        "joinedBaselineCollectionIdList", "newsfeedPages", "catalogEnabled",
        "pollMinFullBarVoteCount", "leaderboardStyle", "facebookAppIdList",
        "welcomeMessage", "welcomeMessageEnabled", "hasPendingReviewRequest",
        "frontPageLayout", "themeColor", "themeHash", "themeVersion", "themeUrl",
        "themeHomePageAppearance", "themeLeftSidePanelTop", "themeLeftSidePanelBottom",
        "themeLeftSidePanelColor", "customList"
    )

    def __init__(self, data: dict):
        self.json = data

        _communtyObjects = tuple(Community(x).Community for x in data)

        if _communtyObjects:
            attributes = tuple(attr for attr in dir(_communtyObjects[0]) if not attr.startswith('__') and not callable(getattr(_communtyObjects[0], attr)) and attr != _communtyObjects[0].__class__.__name__)
            for attr in attributes:
                setattr(self, attr, tuple(getattr(user, attr, None) for user in _communtyObjects))

    @property
    def CommunityList(self):
    
        return self

class CommentList:
    def __init__(self, data):
        self.json = data
        self.author = UserProfileList([y.get("author") for y in data]).UserProfileList
        self.votesSum = tuple(x.get("votesSum") for x in self.json)
        self.votedValue = tuple(x.get("votedValue") for x in self.json)
        self.mediaList = tuple(x.get("mediaList") for x in self.json)
        self.parentComId = tuple(x.get("parentNdcId") for x in self.json)
        self.parentId = tuple(x.get("parentId") for x in self.json)
        self.parentType = tuple(x.get("parentType") for x in self.json)
        self.content = tuple(x.get("content") for x in self.json)
        self.extensions = tuple(x.get("extensions") for x in self.json)
        self.comId = tuple(x.get("ndcId") for x in self.json)
        self.modifiedTime = tuple(x.get("modifiedTime") for x in self.json)
        self.createdTime = tuple(x.get("createdTime") for x in self.json)
        self.commentId = tuple(x.get("commentId") for x in self.json)
        self.subcommentsCount = tuple(x.get("subcommentsCount") for x in self.json)
        self.type = tuple(x.get("type") for x in self.json)

    @property
    def CommentList(self):
        return self


class Membership:
    def __init__(self, data):
        self.json = data
        self.premiumFeature = None
        self.hasAnyAndroidSubscription = None
        self.hasAnyAppleSubscription = None
        self.accountMembership = None
        self.paymentType = None
        self.membershipStatus = None
        self.isAutoRenew = None
        self.createdTime = None
        self.modifiedTime = None
        self.renewedTime = None
        self.expiredTime = None

    @property
    def Membership(self):
        try: self.premiumFeature = self.json["premiumFeatureEnabled"]
        except (KeyError, TypeError): pass
        try: self.hasAnyAndroidSubscription = self.json["hasAnyAndroidSubscription"]
        except (KeyError, TypeError): pass
        try: self.hasAnyAppleSubscription = self.json["hasAnyAppleSubscription"]
        except (KeyError, TypeError): pass
        try: self.accountMembership = self.json["accountMembershipEnabled"]
        except (KeyError, TypeError): pass
        try: self.paymentType = self.json["paymentType"]
        except (KeyError, TypeError): pass
        try: self.membershipStatus = self.json["membership"]["membershipStatus"]
        except (KeyError, TypeError): pass
        try: self.isAutoRenew = self.json["membership"]["isAutoRenew"]
        except (KeyError, TypeError): pass
        try: self.createdTime = self.json["membership"]["createdTime"]
        except (KeyError, TypeError): pass
        try: self.modifiedTime = self.json["membership"]["modifiedTime"]
        except (KeyError, TypeError): pass
        try: self.renewedTime = self.json["membership"]["renewedTime"]
        except (KeyError, TypeError): pass
        try: self.expiredTime = self.json["membership"]["expiredTime"]
        except (KeyError, TypeError): pass

        return self

class FromCode:
    def __init__(self, data):
        self.json = data

        try: self.community: Community = Community(data["extensions"]["community"]).Community
        except (KeyError, TypeError): self.community: Community = Community({})

        self.path = None
        self.objectType = None
        self.shortCode = None
        self.fullPath = None
        self.targetCode = None
        self.objectId = None
        self.shortUrl = None
        self.fullUrl = None
        self.comId = None
        self.comIdPost = None

    @property
    def FromCode(self):
        try: self.path = self.json["path"]
        except (KeyError, TypeError): pass
        try: self.objectType = self.json["extensions"]["linkInfo"]["objectType"]
        except (KeyError, TypeError): pass
        try: self.shortCode = self.json["extensions"]["linkInfo"]["shortCode"]
        except (KeyError, TypeError): pass
        try: self.fullPath = self.json["extensions"]["linkInfo"]["fullPath"]
        except (KeyError, TypeError): pass
        try: self.targetCode = self.json["extensions"]["linkInfo"]["targetCode"]
        except (KeyError, TypeError): pass
        try: self.objectId = self.json["extensions"]["linkInfo"]["objectId"]
        except (KeyError, TypeError): pass
        try: self.shortUrl = self.json["extensions"]["linkInfo"]["shareURLShortCode"]
        except (KeyError, TypeError): pass
        try: self.fullUrl = self.json["extensions"]["linkInfo"]["shareURLFullPath"]
        except (KeyError, TypeError): pass
        try: self.comIdPost = self.json["extensions"]["linkInfo"]["ndcId"]
        except (KeyError, TypeError): pass
        try: self.comId = self.comIdPost or self.json["extensions"]["community"]["ndcId"]
        except (KeyError, TypeError): pass

        return self

class UserProfileCountList:
    __slots__ = (
        "json", "profile", "userProfileCount"
    )

    def __init__(self, data):
        self.json = data

        self.profile: UserProfileList = UserProfileList(data.get("userProfileList")).UserProfileList

        self.userProfileCount = data.get("userProfileCount")

    @property
    def UserProfileCountList(self):

        return self

class UserCheckIns:
    def __init__(self, data):
        self.json = data
        self.hasAnyCheckIn = None
        self.brokenStreaks = None
        self.consecutiveCheckInDays = None

    @property
    def UserCheckIns(self):
        try: self.hasAnyCheckIn = self.json["hasAnyCheckIn"]
        except (KeyError, TypeError): pass
        try: self.brokenStreaks = self.json["brokenStreaks"]
        except (KeyError, TypeError): pass
        try: self.consecutiveCheckInDays = self.json["consecutiveCheckInDays"]
        except (KeyError, TypeError): pass

        return self

class WalletInfo:
    def __init__(self, data):
        self.json = data
        self.totalCoinsFloat = None
        self.adsEnabled = None
        self.adsVideoStats = None
        self.adsFlags = None
        self.totalCoins = None
        self.businessCoinsEnabled = None
        self.totalBusinessCoins = None
        self.totalBusinessCoinsFloat = None

    @property
    def WalletInfo(self):
        try: self.totalCoinsFloat = self.json["totalCoinsFloat"]
        except (KeyError, TypeError): pass
        try: self.adsEnabled = self.json["adsEnabled"]
        except (KeyError, TypeError): pass
        try: self.adsVideoStats = self.json["adsVideoStats"]
        except (KeyError, TypeError): pass
        try: self.adsFlags = self.json["adsFlags"]
        except (KeyError, TypeError): pass
        try: self.totalCoins = self.json["totalCoins"]
        except (KeyError, TypeError): pass
        try: self.businessCoinsEnabled = self.json["businessCoinsEnabled"]
        except (KeyError, TypeError): pass
        try: self.totalBusinessCoins = self.json["totalBusinessCoins"]
        except (KeyError, TypeError): pass
        try: self.totalBusinessCoinsFloat = self.json["totalBusinessCoinsFloat"]
        except (KeyError, TypeError): pass

        return self

class WalletHistory:
    def __init__(self, data):
        self.json = data
        self.taxCoins = []
        self.bonusCoinsFloat = []
        self.isPositive = []
        self.bonusCoins = []
        self.taxCoinsFloat = []
        self.transanctionId = []
        self.changedCoins = []
        self.totalCoinsFloat = []
        self.changedCoinsFloat = []
        self.sourceType = []
        self.createdTime = []
        self.totalCoins = []
        self.originCoinsFloat = []
        self.originCoins = []
        self.extData = []
        self.title = []
        self.description = []
        self.icon = []
        self.objectDeeplinkUrl = []
        self.sourceIp = []

    @property
    def WalletHistory(self):
        for x in self.json:
            try: self.taxCoins.append(x["taxCoins"])
            except (KeyError, TypeError): self.taxCoins.append(None)
            try: self.bonusCoinsFloat.append(x["bonusCoinsFloat"])
            except (KeyError, TypeError): self.bonusCoinsFloat.append(None)
            try: self.isPositive.append(x["isPositive"])
            except (KeyError, TypeError): self.isPositive.append(None)
            try: self.bonusCoins.append(x["bonusCoins"])
            except (KeyError, TypeError): self.bonusCoins.append(None)
            try: self.taxCoinsFloat.append(x["taxCoinsFloat"])
            except (KeyError, TypeError): self.taxCoinsFloat.append(None)
            try: self.transanctionId.append(x["uid"])
            except (KeyError, TypeError): self.transanctionId.append(None)
            try: self.changedCoins.append(x["changedCoins"])
            except (KeyError, TypeError): self.changedCoins.append(None)
            try: self.totalCoinsFloat.append(x["totalCoinsFloat"])
            except (KeyError, TypeError): self.totalCoinsFloat.append(None)
            try: self.changedCoinsFloat.append(x["changedCoinsFloat"])
            except (KeyError, TypeError): self.changedCoinsFloat.append(None)
            try: self.sourceType.append(x["sourceType"])
            except (KeyError, TypeError): self.sourceType.append(None)
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)
            try: self.totalCoins.append(x["totalCoins"])
            except (KeyError, TypeError): self.totalCoins.append(None)
            try: self.originCoinsFloat.append(x["originCoinsFloat"])
            except (KeyError, TypeError): self.originCoinsFloat.append(None)
            try: self.originCoins.append(x["originCoins"])
            except (KeyError, TypeError): self.originCoins.append(None)
            try: self.extData.append(x["extData"])
            except (KeyError, TypeError): self.extData.append(None)
            try: self.title.append(x["extData"]["description"])
            except (KeyError, TypeError): self.title.append(None)
            try: self.icon.append(x["extData"]["icon"])
            except (KeyError, TypeError): self.icon.append(None)
            try: self.description.append(x["extData"]["subtitle"])
            except (KeyError, TypeError): self.description.append(None)
            try: self.objectDeeplinkUrl.append(x["extData"]["objectDeeplinkUrl"])
            except (KeyError, TypeError): self.objectDeeplinkUrl.append(None)
            try: self.sourceIp.append(x["extData"]["sourceIp"])
            except (KeyError, TypeError): self.sourceIp.append(None)

        return self


class UserAchievements:
    def __init__(self, data):
        self.json = data
        self.secondsSpentOfLast24Hours = None
        self.secondsSpentOfLast7Days = None
        self.numberOfFollowersCount = None
        self.numberOfPostsCreated = None

    @property
    def UserAchievements(self):
        try: self.secondsSpentOfLast24Hours = self.json["secondsSpentOfLast24Hours"]
        except (KeyError, TypeError): pass
        try: self.secondsSpentOfLast7Days = self.json["secondsSpentOfLast7Days"]
        except (KeyError, TypeError): pass
        try: self.numberOfFollowersCount = self.json["numberOfMembersCount"]
        except (KeyError, TypeError): pass
        try: self.numberOfPostsCreated = self.json["numberOfPostsCreated"]
        except (KeyError, TypeError): pass

        return self

class UserSavedBlogs:
    def __init__(self, data):
        _object = []

        self.json = data

        for y in data:
            if y["refObjectType"] == 1:
                try: _object.append(Blog(y["refObject"]).Blog)
                except (KeyError, TypeError): _object.append(None)

            elif y["refObjectType"] == 2:
                try: _object.append(Wiki(y["refObject"]).Wiki)
                except (KeyError, TypeError): _object.append(None)

            else:
                try: _object.append(y["refObject"])
                except (KeyError, TypeError): _object.append(None)

        self.object = _object
        self.objectType = []
        self.bookmarkedTime = []
        self.objectId = []
        self.objectJson = []

    @property
    def UserSavedBlogs(self):
        for x in self.json:
            try: self.objectType.append(x["refObjectType"])
            except (KeyError, TypeError): self.objectType.append(None)
            try: self.bookmarkedTime.append(x["bookmarkedTime"])
            except (KeyError, TypeError): self.bookmarkedTime.append(None)
            try: self.objectId.append(x["refObjectId"])
            except (KeyError, TypeError): self.objectId.append(None)
            try: self.objectJson.append(x["refObject"])
            except (KeyError, TypeError): self.objectJson.append(None)

        return self

class GetWikiInfo:
    def __init__(self, data):
        self.json = data

        try: self.wiki: Wiki = Wiki(data["item"]).Wiki
        except (KeyError, TypeError): self.wiki: Wiki = Wiki([])

        self.inMyFavorites = None
        self.isBookmarked = None

    @property
    def GetWikiInfo(self):
        try: self.inMyFavorites = self.json["inMyFavorites"]
        except (KeyError, TypeError): pass
        try: self.isBookmarked = self.json["isBookmarked"]
        except (KeyError, TypeError): pass

        return self

class GetBlogInfo:
    def __init__(self, data):
        self.json = data

        try: self.blog: Blog = Blog(data["blog"]).Blog
        except (KeyError, TypeError): self.blog: Blog = Blog([])

        self.isBookmarked = None

    @property
    def GetBlogInfo(self):
        try: self.isBookmarked = self.json["isBookmarked"]
        except (KeyError, TypeError): pass

        return self

class GetSharedFolderInfo:
    def __init__(self, data):
        self.json = data
        self.folderCount = None
        self.fileCount = None

    @property
    def GetSharedFolderInfo(self):
        try: self.folderCount = self.json["folderCount"]
        except (KeyError, TypeError): pass
        try: self.fileCount = self.json["fileCount"]
        except (KeyError, TypeError): pass

        return self

class WikiCategoryList:
    def __init__(self, data):
        _categoryObjects = tuple(WikiCategory(x).WikiCategory for x in data)

        if _categoryObjects:
            attributes = tuple(attr for attr in dir(_categoryObjects[0]) if not attr.startswith('__') and not callable(getattr(_categoryObjects[0], attr)) and attr != _categoryObjects[0].__class__.__name__)
            for attr in attributes:
                setattr(self, attr, tuple(getattr(user, attr, None) for user in _categoryObjects))

    @property
    def WikiCategoryList(self):

        return self

class WikiCategory:
    def __init__(self, data):
        self.json = data

        try: self.author = UserProfile(data["itemCategory"]["author"]).UserProfile
        except (KeyError, TypeError): self.author: UserProfile = UserProfile([])
        try: self.subCategory = WikiCategoryList(data["childrenWrapper"]["itemCategoryList"]).WikiCategoryList
        except (KeyError, TypeError): self.subCategory: WikiCategoryList = WikiCategoryList([])

        self.itemsCount = None
        self.parentCategoryId = None
        self.parentType = None
        self.categoryId = None
        self.content = None
        self.extensions = None
        self.createdTime = None
        self.subcategoriesCount = None
        self.title = None
        self.mediaList = None
        self.icon = None

    @property
    def WikiCategory(self):
        try: self.itemsCount = self.json["itemCategory"]["itemsCount"]
        except (KeyError, TypeError): pass
        try: self.parentCategoryId = self.json["itemCategory"]["parentCategoryId"]
        except (KeyError, TypeError): pass
        try: self.categoryId = self.json["itemCategory"]["categoryId"]
        except (KeyError, TypeError): pass
        try: self.extensions = self.json["itemCategory"]["extensions"]
        except (KeyError, TypeError): pass
        try: self.createdTime = self.json["itemCategory"]["createdTime"]
        except (KeyError, TypeError): pass
        try: self.title = self.json["itemCategory"]["label"]
        except (KeyError, TypeError): pass
        try: self.mediaList = self.json["itemCategory"]["mediaList"]
        except (KeyError, TypeError): pass
        try: self.icon = self.json["itemCategory"]["icon"]
        except (KeyError, TypeError): pass
        try: self.parentType = self.json["childrenWrapper"]["type"]
        except (KeyError, TypeError): pass

        return self

class TippedUsersSummary:
    def __init__(self, data):
        _author = []

        self.json = data

        for y in data["tippedUserList"]:
            try: _author.append(y["tipper"])
            except (KeyError, TypeError): _author.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.tipSummary = None
        self.totalCoins = None
        self.tippersCount = None
        self.globalTipSummary = None
        self.globalTippersCount = None
        self.globalTotalCoins = None
        self.lastTippedTime = []
        self.totalTippedCoins = []
        self.lastThankedTime = []

    @property
    def TippedUsersSummary(self):
        try: self.tipSummary = self.json["tipSummary"]
        except (KeyError, TypeError): pass
        try: self.totalCoins = self.json["tipSummary"]["totalCoins"]
        except (KeyError, TypeError): pass
        try: self.tippersCount = self.json["tipSummary"]["tippersCount"]
        except (KeyError, TypeError): pass
        try: self.globalTipSummary = self.json["globalTipSummary"]
        except (KeyError, TypeError): pass
        try: self.globalTippersCount = self.json["globalTipSummary"]["tippersCount"]
        except (KeyError, TypeError): pass
        try: self.globalTotalCoins = self.json["globalTipSummary"]["totalCoins"]
        except (KeyError, TypeError): pass

        for tippedUserList in self.json["tippedUserList"]:
            try: self.lastTippedTime.append(tippedUserList["lastTippedTime"])
            except (KeyError, TypeError): self.lastTippedTime.append(None)
            try: self.totalTippedCoins.append(tippedUserList["totalTippedCoins"])
            except (KeyError, TypeError): self.totalTippedCoins.append(None)
            try: self.lastThankedTime.append(tippedUserList["lastThankedTime"])
            except (KeyError, TypeError): self.lastThankedTime.append(None)

        return self

class Thread:
    def __init__(self, data):
        self.json = data

        try: self.author: UserProfile = UserProfile(data["author"]).UserProfile
        except (KeyError, TypeError): self.author: UserProfile = UserProfile([])
        try: self.membersSummary: UserProfileList = UserProfileList(data["membersSummary"]).UserProfileList
        except (KeyError, TypeError): self.membersSummary: UserProfileList = UserProfileList([])

        self.userAddedTopicList = None
        self.membersQuota = None
        self.chatId = None
        self.keywords = None
        self.membersCount = None
        self.isPinned = None
        self.title = None
        self.membershipStatus = None
        self.content = None
        self.needHidden = None
        self.alertOption = None
        self.lastReadTime = None
        self.type = None
        self.status = None
        self.publishToGlobal = None
        self.modifiedTime = None
        self.condition = None
        self.icon = None
        self.latestActivityTime = None
        self.extensions = None
        self.viewOnly = None
        self.coHosts = None
        self.membersCanInvite = None
        self.announcement = None
        self.language = None
        self.lastMembersSummaryUpdateTime = None
        self.backgroundImage = None
        self.channelType = None
        self.comId = None
        self.createdTime = None
        self.creatorId = None
        self.bannedUsers = None
        self.tippingPermStatus = None
        self.visibility = None
        self.fansOnly = None
        self.pinAnnouncement = None
        self.vvChatJoinType = None
        self.screeningRoomHostId = None
        self.screeningRoomPermission = None
        self.disabledTime = None
        self.organizerTransferCreatedTime = None
        self.organizerTransferId = None

    @property
    def Thread(self):
        try: self.userAddedTopicList = self.json["userAddedTopicList"]
        except (KeyError, TypeError): pass
        try: self.membersQuota = self.json["membersQuota"]
        except (KeyError, TypeError): pass
        try: self.chatId = self.json["threadId"]
        except (KeyError, TypeError): pass
        try: self.keywords = self.json["keywords"]
        except (KeyError, TypeError): pass
        try: self.membersCount = self.json["membersCount"]
        except (KeyError, TypeError): pass
        try: self.isPinned = self.json["isPinned"]
        except (KeyError, TypeError): pass
        try: self.title = self.json["title"]
        except (KeyError, TypeError): pass
        try: self.membershipStatus = self.json["membershipStatus"]
        except (KeyError, TypeError): pass
        try: self.content = self.json["content"]
        except (KeyError, TypeError): pass
        try: self.needHidden = self.json["needHidden"]
        except (KeyError, TypeError): pass
        try: self.alertOption = self.json["alertOption"]
        except (KeyError, TypeError): pass
        try: self.lastReadTime = self.json["lastReadTime"]
        except (KeyError, TypeError): pass
        try: self.type = self.json["type"]
        except (KeyError, TypeError): pass
        try: self.status = self.json["status"]
        except (KeyError, TypeError): pass
        try: self.publishToGlobal = self.json["publishToGlobal"]
        except (KeyError, TypeError): pass
        try: self.modifiedTime = self.json["modifiedTime"]
        except (KeyError, TypeError): pass
        try: self.condition = self.json["condition"]
        except (KeyError, TypeError): pass
        try: self.icon = self.json["icon"]
        except (KeyError, TypeError): pass
        try: self.latestActivityTime = self.json["latestActivityTime"]
        except (KeyError, TypeError): pass
        try: self.comId = self.json["ndcId"]
        except (KeyError, TypeError): pass
        try: self.createdTime = self.json["createdTime"]
        except (KeyError, TypeError): pass
        try: self.extensions = self.json["extensions"]
        except (KeyError, TypeError): pass
        try: self.viewOnly = self.json["extensions"]["viewOnly"]
        except (KeyError, TypeError): pass
        try: self.coHosts = self.json["extensions"]["coHost"]
        except (KeyError, TypeError): pass
        try: self.membersCanInvite = self.json["extensions"]["membersCanInvite"]
        except (KeyError, TypeError): pass
        try: self.language = self.json["extensions"]["language"]
        except (KeyError, TypeError): pass
        try: self.announcement = self.json["extensions"]["announcement"]
        except (KeyError, TypeError): pass
        try: self.backgroundImage = self.json["extensions"]["bm"][1]
        except (KeyError, TypeError, IndexError): pass
        try: self.lastMembersSummaryUpdateTime = self.json["extensions"]["lastMembersSummaryUpdateTime"]
        except (KeyError, TypeError): pass
        try: self.channelType = self.json["extensions"]["channelType"]
        except (KeyError, TypeError): pass
        try: self.creatorId = self.json["extensions"]["creatorUid"]
        except (KeyError, TypeError): pass
        try: self.bannedUsers = self.json["extensions"]["bannedMemberUidList"]
        except (KeyError, TypeError): pass
        try: self.visibility = self.json["extensions"]["visibility"]
        except (KeyError, TypeError): pass
        try: self.fansOnly = self.json["extensions"]["fansOnly"]
        except (KeyError, TypeError): pass
        try: self.pinAnnouncement = self.json["extensions"]["pinAnnouncement"]
        except (KeyError, TypeError): pass
        try: self.vvChatJoinType = self.json["extensions"]["vvChatJoinType"]
        except (KeyError, TypeError): pass
        try: self.disabledTime = self.json["extensions"]["__disabledTime__"]
        except (KeyError, TypeError): pass
        try: self.tippingPermStatus = self.json["extensions"]["tippingPermStatus"]
        except (KeyError, TypeError): pass
        try: self.screeningRoomHostId = self.json["extensions"]["screeningRoomHostUid"]
        except (KeyError, TypeError): pass
        try: self.screeningRoomPermission = self.json["extensions"]["screeningRoomPermission"]["action"]
        except (KeyError, TypeError): pass
        try: self.organizerTransferCreatedTime = self.json["extensions"]["organizerTransferRequest"]["createdTime"]
        except (KeyError, TypeError): pass
        try: self.organizerTransferId = self.json["extensions"]["organizerTransferRequest"]["requestId"]
        except (KeyError, TypeError): pass

        return self

class ThreadList:
    def __init__(self, data):
        _author, _membersSummary = [], []

        self.json = data

        for y in data:
            try: _author.append(y["author"])
            except (KeyError, TypeError): _author.append(None)

            try: _membersSummary.append(UserProfileList(y["membersSummary"]).UserProfileList)
            except (KeyError, TypeError): _membersSummary.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.membersSummary = _membersSummary
        self.userAddedTopicList = []
        self.membersQuota = []
        self.chatId = []
        self.keywords = []
        self.membersCount = []
        self.isPinned = []
        self.title = []
        self.membershipStatus = []
        self.content = []
        self.needHidden = []
        self.alertOption = []
        self.lastReadTime = []
        self.type = []
        self.status = []
        self.publishToGlobal = []
        self.modifiedTime = []
        self.condition = []
        self.icon = []
        self.latestActivityTime = []
        self.extensions = []
        self.viewOnly = []
        self.coHosts = []
        self.membersCanInvite = []
        self.announcement = []
        self.language = []
        self.lastMembersSummaryUpdateTime = []
        self.backgroundImage = []
        self.channelType = []
        self.comId = []
        self.createdTime = []
        self.creatorId = []
        self.bannedUsers = []
        self.tippingPermStatus = []
        self.visibility = []
        self.fansOnly = []
        self.pinAnnouncement = []
        self.vvChatJoinType = []
        self.screeningRoomHostId = []
        self.screeningRoomPermission = []
        self.disabledTime = []
        self.organizerTransferCreatedTime = []
        self.organizerTransferId = []

    @property
    def ThreadList(self):
        for chat in self.json:
            try: self.userAddedTopicList.append(chat["userAddedTopicList"])
            except (KeyError, TypeError): self.userAddedTopicList.append(None)
            try: self.membersQuota.append(chat["membersQuota"])
            except (KeyError, TypeError): self.membersQuota.append(None)
            try: self.chatId.append(chat["threadId"])
            except (KeyError, TypeError): self.chatId.append(None)
            try: self.keywords.append(chat["keywords"])
            except (KeyError, TypeError): self.keywords.append(None)
            try: self.membersCount.append(chat["membersCount"])
            except (KeyError, TypeError): self.membersCount.append(None)
            try: self.isPinned.append(chat["isPinned"])
            except (KeyError, TypeError): self.isPinned.append(None)
            try: self.title.append(chat["title"])
            except (KeyError, TypeError): self.title.append(None)
            try: self.membershipStatus.append(chat["membershipStatus"])
            except (KeyError, TypeError): self.membershipStatus.append(None)
            try: self.content.append(chat["content"])
            except (KeyError, TypeError): self.content.append(None)
            try: self.needHidden.append(chat["needHidden"])
            except (KeyError, TypeError): self.needHidden.append(None)
            try: self.alertOption.append(chat["alertOption"])
            except (KeyError, TypeError): self.alertOption.append(None)
            try: self.lastReadTime.append(chat["lastReadTime"])
            except (KeyError, TypeError): self.lastReadTime.append(None)
            try: self.type.append(chat["type"])
            except (KeyError, TypeError): self.type.append(None)
            try: self.status.append(chat["status"])
            except (KeyError, TypeError): self.status.append(None)
            try: self.publishToGlobal.append(chat["publishToGlobal"])
            except (KeyError, TypeError): self.publishToGlobal.append(None)
            try: self.modifiedTime.append(chat["modifiedTime"])
            except (KeyError, TypeError): self.modifiedTime.append(None)
            try: self.condition.append(chat["condition"])
            except (KeyError, TypeError): self.condition.append(None)
            try: self.icon.append(chat["icon"])
            except (KeyError, TypeError): self.icon.append(None)
            try: self.latestActivityTime.append(chat["latestActivityTime"])
            except (KeyError, TypeError): self.latestActivityTime.append(None)
            try: self.comId.append(chat["ndcId"])
            except (KeyError, TypeError): self.comId.append(None)
            try: self.createdTime.append(chat["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)
            try:  self.extensions.append(chat["extensions"])
            except (KeyError, TypeError): self.extensions.append(None)
            try:  self.viewOnly.append(chat["extensions"]["viewOnly"])
            except (KeyError, TypeError): self.viewOnly.append(None)
            try:  self.coHosts.append(chat["extensions"]["coHost"])
            except (KeyError, TypeError): self.coHosts.append(None)
            try:  self.membersCanInvite.append(chat["extensions"]["membersCanInvite"])
            except (KeyError, TypeError): self.membersCanInvite.append(None)
            try:  self.language.append(chat["extensions"]["language"])
            except (KeyError, TypeError): self.language.append(None)
            try:  self.announcement.append(chat["extensions"]["announcement"])
            except (KeyError, TypeError): self.announcement.append(None)
            try:  self.backgroundImage.append(chat["extensions"]["bm"][1])
            except (KeyError, TypeError, IndexError): self.backgroundImage.append(None)
            try:  self.lastMembersSummaryUpdateTime.append(chat["extensions"]["lastMembersSummaryUpdateTime"])
            except (KeyError, TypeError): self.lastMembersSummaryUpdateTime.append(None)
            try:  self.channelType.append(chat["extensions"]["channelType"])
            except (KeyError, TypeError): self.channelType.append(None)
            try:  self.creatorId.append(chat["extensions"]["creatorUid"])
            except (KeyError, TypeError): self.creatorId.append(None)
            try:  self.bannedUsers.append(chat["extensions"]["bannedMemberUidList"])
            except (KeyError, TypeError): self.bannedUsers.append(None)
            try:  self.visibility.append(chat["extensions"]["visibility"])
            except (KeyError, TypeError): self.visibility.append(None)
            try:  self.fansOnly.append(chat["extensions"]["fansOnly"])
            except (KeyError, TypeError): self.fansOnly.append(None)
            try:  self.pinAnnouncement.append(chat["extensions"]["pinAnnouncement"])
            except (KeyError, TypeError): self.pinAnnouncement.append(None)
            try:  self.vvChatJoinType.append(chat["extensions"]["vvChatJoinType"])
            except (KeyError, TypeError): self.vvChatJoinType.append(None)
            try:  self.tippingPermStatus.append(chat["extensions"]["tippingPermStatus"])
            except (KeyError, TypeError): self.tippingPermStatus.append(None)
            try:  self.screeningRoomHostId.append(chat["extensions"]["screeningRoomHostUid"])
            except (KeyError, TypeError): self.screeningRoomHostId.append(None)
            try:  self.disabledTime.append(chat["extensions"]["__disabledTime__"])
            except (KeyError, TypeError): self.disabledTime.append(None)
            try:  self.screeningRoomPermission.append(chat["extensions"]["screeningRoomPermission"]["action"])
            except (KeyError, TypeError): self.screeningRoomPermission.append(None)
            try:  self.organizerTransferCreatedTime.append(chat["extensions"]["organizerTransferRequest"]["createdTime"])
            except (KeyError, TypeError): self.organizerTransferCreatedTime.append(None)
            try:  self.organizerTransferId.append(chat["extensions"]["organizerTransferRequest"]["requestId"])
            except (KeyError, TypeError): self.organizerTransferId.append(None)

        return self

class Sticker:
    def __init__(self, data):
        self.json = data

        try: self.collection: StickerCollection = StickerCollection(data["stickerCollectionSummary"]).StickerCollection
        except (KeyError, TypeError): self.collection: StickerCollection = StickerCollection([])

        self.status = None
        self.icon = None
        self.iconV2 = None
        self.name = None
        self.stickerId = None
        self.smallIcon = None
        self.smallIconV2 = None
        self.stickerCollectionId = None
        self.mediumIcon = None
        self.mediumIconV2 = None
        self.extensions = None
        self.usedCount = None
        self.createdTime = None

    @property
    def Sticker(self):
        try: self.status = self.json["status"]
        except (KeyError, TypeError): pass
        try: self.icon = self.json["icon"]
        except (KeyError, TypeError): pass
        try: self.iconV2 = self.json["iconV2"]
        except (KeyError, TypeError): pass
        try: self.name = self.json["name"]
        except (KeyError, TypeError): pass
        try: self.stickerId = self.json["stickerId"]
        except (KeyError, TypeError): pass
        try: self.smallIcon = self.json["smallIcon"]
        except (KeyError, TypeError): pass
        try: self.smallIconV2 = self.json["smallIconV2"]
        except (KeyError, TypeError): pass
        try: self.stickerCollectionId = self.json["stickerCollectionId"]
        except (KeyError, TypeError): pass
        try: self.mediumIcon = self.json["mediumIcon"]
        except (KeyError, TypeError): pass
        try: self.mediumIconV2 = self.json["mediumIconV2"]
        except (KeyError, TypeError): pass
        try: self.extensions = self.json["extensions"]
        except (KeyError, TypeError): pass
        try: self.usedCount = self.json["usedCount"]
        except (KeyError, TypeError): pass
        try: self.createdTime = self.json["createdTime"]
        except (KeyError, TypeError): pass

        return self

class StickerList:
    def __init__(self, data):
        _collection = []

        self.json = data

        for y in data:
            try: _collection.append(y["stickerCollectionSummary"])
            except (KeyError, TypeError): _collection.append(None)

        self.collection: StickerCollectionList = StickerCollectionList(_collection).StickerCollectionList
        self.status = []
        self.icon = []
        self.iconV2 = []
        self.name = []
        self.stickerId = []
        self.smallIcon = []
        self.smallIconV2 = []
        self.stickerCollectionId = []
        self.mediumIcon = []
        self.mediumIconV2 = []
        self.extensions = []
        self.usedCount = []
        self.createdTime = []

    @property
    def StickerList(self):
        for x in self.json:
            try: self.status.append(x["status"])
            except (KeyError, TypeError): self.status.append(None)
            try: self.icon.append(x["icon"])
            except (KeyError, TypeError): self.icon.append(None)
            try: self.iconV2.append(x["iconV2"])
            except (KeyError, TypeError): self.iconV2.append(None)
            try: self.name.append(x["name"])
            except (KeyError, TypeError): self.name.append(None)
            try: self.stickerId.append(x["stickerId"])
            except (KeyError, TypeError): self.stickerId.append(None)
            try: self.smallIcon.append(x["smallIcon"])
            except (KeyError, TypeError): self.smallIcon.append(None)
            try: self.smallIconV2.append(x["smallIconV2"])
            except (KeyError, TypeError): self.smallIconV2.append(None)
            try: self.stickerCollectionId.append(x["stickerCollectionId"])
            except (KeyError, TypeError): self.stickerCollectionId.append(None)
            try: self.mediumIcon.append(x["mediumIcon"])
            except (KeyError, TypeError): self.mediumIcon.append(None)
            try: self.mediumIconV2.append(x["mediumIconV2"])
            except (KeyError, TypeError): self.mediumIconV2.append(None)
            try: self.extensions.append(x["extensions"])
            except (KeyError, TypeError): self.extensions.append(None)
            try: self.usedCount.append(x["usedCount"])
            except (KeyError, TypeError): self.usedCount.append(None)
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)

        return self

class StickerCollection:
    def __init__(self, data):
        self.json = data

        try: self.author: UserProfile = UserProfile(data["author"]).UserProfile
        except (KeyError, TypeError): self.author: UserProfile = UserProfile([])
        try: self.originalAuthor: UserProfile = UserProfile(data["extensions"]["originalAuthor"]).UserProfile
        except (KeyError, TypeError): self.originalAuthor: UserProfile = UserProfile([])
        try: self.originalCommunity: Community = Community(data["extensions"]["originalCommunity"]).Community
        except (KeyError, TypeError): self.originalCommunity: Community = Community([])

        self.status = None
        self.collectionType = None
        self.modifiedTime = None
        self.bannerUrl = None
        self.smallIcon = None
        self.stickersCount = None
        self.usedCount = None
        self.icon = None
        self.title = None
        self.collectionId = None
        self.extensions = None
        self.isActivated = None
        self.ownershipStatus = None
        self.isNew = None
        self.availableComIds = None
        self.description = None
        self.iconSourceStickerId = None
        self.restrictionInfo = None
        self.discountValue = None
        self.discountStatus = None
        self.ownerId = None
        self.ownerType = None
        self.restrictType = None
        self.restrictValue = None
        self.availableDuration = None

    @property
    def StickerCollection(self):
        try: self.status = self.json["status"]
        except (KeyError, TypeError): pass
        try: self.collectionType = self.json["collectionType"]
        except (KeyError, TypeError): pass
        try: self.modifiedTime = self.json["modifiedTime"]
        except (KeyError, TypeError): pass
        try: self.bannerUrl = self.json["bannerUrl"]
        except (KeyError, TypeError): pass
        try: self.smallIcon = self.json["smallIcon"]
        except (KeyError, TypeError): pass
        try: self.stickersCount = self.json["stickersCount"]
        except (KeyError, TypeError): pass
        try: self.usedCount = self.json["usedCount"]
        except (KeyError, TypeError): pass
        try: self.icon = self.json["icon"]
        except (KeyError, TypeError): pass
        try: self.title = self.json["name"]
        except (KeyError, TypeError): pass
        try: self.collectionId = self.json["collectionId"]
        except (KeyError, TypeError): pass
        try: self.extensions = self.json["extensions"]
        except (KeyError, TypeError): pass
        try: self.iconSourceStickerId = self.json["extensions"]["iconSourceStickerId"]
        except (KeyError, TypeError): pass
        try: self.isActivated = self.json["isActivated"]
        except (KeyError, TypeError): pass
        try: self.ownershipStatus = self.json["ownershipStatus"]
        except (KeyError, TypeError): pass
        try: self.isNew = self.json["isNew"]
        except (KeyError, TypeError): pass
        try: self.availableComIds = self.json["availableNdcIds"]
        except (KeyError, TypeError): pass
        try: self.description = self.json["description"]
        except (KeyError, TypeError): pass
        try: self.restrictionInfo = self.json["restrictionInfo"]
        except (KeyError, TypeError): pass
        try: self.discountStatus = self.json["restrictionInfo"]["discountStatus"]
        except (KeyError, TypeError): pass
        try: self.discountValue = self.json["restrictionInfo"]["discountValue"]
        except (KeyError, TypeError): pass
        try: self.ownerId = self.json["restrictionInfo"]["ownerUid"]
        except (KeyError, TypeError): pass
        try: self.ownerType = self.json["restrictionInfo"]["ownerType"]
        except (KeyError, TypeError): pass
        try: self.restrictType = self.json["restrictionInfo"]["restrictType"]
        except (KeyError, TypeError): pass
        try: self.restrictValue = self.json["restrictionInfo"]["restrictValue"]
        except (KeyError, TypeError): pass
        try: self.availableDuration = self.json["restrictionInfo"]["availableDuration"]
        except (KeyError, TypeError): pass

        return self

class StickerCollectionList:
    def __init__(self, data):
        _author, _originalAuthor, _originalCommunity = [], [], []

        self.json = data

        for y in data:
            try: _author.append(y["author"])
            except (KeyError, TypeError): _author.append(None)
            try: _originalAuthor.append(y["extensions"]["originalAuthor"])
            except (KeyError, TypeError): _originalAuthor.append(None)
            try: _originalCommunity.append(y["extensions"]["originalCommunity"])
            except (KeyError, TypeError): _originalCommunity.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.originalAuthor: UserProfileList = UserProfileList(_originalAuthor).UserProfileList
        self.originalCommunity: CommunityList = CommunityList(_originalCommunity).CommunityList
        self.status = []
        self.collectionType = []
        self.modifiedTime = []
        self.bannerUrl = []
        self.smallIcon = []
        self.stickersCount = []
        self.usedCount = []
        self.icon = []
        self.name = []
        self.collectionId = []
        self.extensions = []
        self.isActivated = []
        self.ownershipStatus = []
        self.isNew = []
        self.availableComIds = []
        self.description = []
        self.iconSourceStickerId = []
        self.restrictionInfo = []
        self.discountValue = []
        self.discountStatus = []
        self.ownerId = []
        self.ownerType = []
        self.restrictType = []
        self.restrictValue = []
        self.availableDuration = []

    @property
    def StickerCollectionList(self):
        for x in self.json:
            try: self.status.append(x["status"])
            except (KeyError, TypeError): self.status.append(None)
            try: self.collectionType.append(x["collectionType"])
            except (KeyError, TypeError): self.collectionType.append(None)
            try: self.modifiedTime.append(x["modifiedTime"])
            except (KeyError, TypeError): self.modifiedTime.append(None)
            try: self.bannerUrl.append(x["bannerUrl"])
            except (KeyError, TypeError): self.bannerUrl.append(None)
            try: self.smallIcon.append(x["smallIcon"])
            except (KeyError, TypeError): self.smallIcon.append(None)
            try: self.stickersCount.append(x["stickersCount"])
            except (KeyError, TypeError): self.stickersCount.append(None)
            try: self.usedCount.append(x["usedCount"])
            except (KeyError, TypeError): self.usedCount.append(None)
            try: self.icon.append(x["icon"])
            except (KeyError, TypeError): self.icon.append(None)
            try: self.name.append(x["name"])
            except (KeyError, TypeError): self.name.append(None)
            try: self.collectionId.append(x["collectionId"])
            except (KeyError, TypeError): self.collectionId.append(None)
            try: self.extensions.append(x["extensions"])
            except (KeyError, TypeError): self.extensions.append(None)
            try: self.iconSourceStickerId.append(x["extensions"]["iconSourceStickerId"])
            except (KeyError, TypeError): self.iconSourceStickerId.append(None)
            try: self.isActivated.append(x["isActivated"])
            except (KeyError, TypeError): self.isActivated.append(None)
            try: self.ownershipStatus.append(x["ownershipStatus"])
            except (KeyError, TypeError): self.ownershipStatus.append(None)
            try: self.isNew.append(x["isNew"])
            except (KeyError, TypeError): self.isNew.append(None)
            try: self.availableComIds.append(x["availableNdcIds"])
            except (KeyError, TypeError): self.availableComIds.append(None)
            try: self.description.append(x["description"])
            except (KeyError, TypeError): self.description.append(None)
            try: self.restrictionInfo.append(x["restrictionInfo"])
            except (KeyError, TypeError): self.restrictionInfo.append(None)
            try: self.discountStatus.append(x["restrictionInfo"]["discountStatus"])
            except (KeyError, TypeError): self.discountStatus.append(None)
            try: self.discountValue.append(x["restrictionInfo"]["discountValue"])
            except (KeyError, TypeError): self.discountValue.append(None)
            try: self.ownerId.append(x["restrictionInfo"]["ownerUid"])
            except (KeyError, TypeError): self.ownerId.append(None)
            try: self.ownerType.append(x["restrictionInfo"]["ownerType"])
            except (KeyError, TypeError): self.ownerType.append(None)
            try: self.restrictType.append(x["restrictionInfo"]["restrictType"])
            except (KeyError, TypeError): self.restrictType.append(None)
            try: self.restrictValue.append(x["restrictionInfo"]["restrictValue"])
            except (KeyError, TypeError): self.restrictValue.append(None)
            try: self.availableDuration.append(x["restrictionInfo"]["availableDuration"])
            except (KeyError, TypeError): self.availableDuration.append(None)

        return self

class Message:
    def __init__(self, data):
        self.json = data

        try: self.author: UserProfile = UserProfile(data["author"]).UserProfile
        except (KeyError, TypeError): self.author: UserProfile = UserProfile([])
        try: self.sticker: Sticker = Sticker(data["extensions"]["sticker"]).Sticker
        except (KeyError, TypeError): self.sticker: Sticker = Sticker([])

        self.content = None
        self.includedInSummary = None
        self.isHidden = None
        self.messageType = None
        self.messageId = None
        self.mediaType = None
        self.mediaValue = None
        self.chatBubbleId = None
        self.clientRefId = None
        self.chatId = None
        self.createdTime = None
        self.chatBubbleVersion = None
        self.type = None
        self.replyMessage = None
        self.extensions = None
        self.duration = None
        self.originalStickerId = None
        self.videoDuration = None
        self.videoExtensions = None
        self.videoHeight = None
        self.videoCoverImage = None
        self.videoWidth = None
        self.mentionUserIds = None
        self.tippingCoins = None


    @property
    def Message(self):
        try: self.content = self.json["content"]
        except (KeyError, TypeError): pass
        try: self.includedInSummary = self.json["includedInSummary"]
        except (KeyError, TypeError): pass
        try: self.isHidden = self.json["isHidden"]
        except (KeyError, TypeError): pass
        try: self.messageId = self.json["messageId"]
        except (KeyError, TypeError): pass
        try: self.messageType = self.json["messageType"]
        except (KeyError, TypeError): pass
        try: self.mediaType = self.json["mediaType"]
        except (KeyError, TypeError): pass
        try: self.chatBubbleId = self.json["chatBubbleId"]
        except (KeyError, TypeError): pass
        try: self.clientRefId = self.json["clientRefId"]
        except (KeyError, TypeError): pass
        try: self.chatId = self.json["threadId"]
        except (KeyError, TypeError): pass
        try: self.createdTime = self.json["createdTime"]
        except (KeyError, TypeError): pass
        try: self.chatBubbleVersion = self.json["chatBubbleVersion"]
        except (KeyError, TypeError): pass
        try: self.type = self.json["type"]
        except (KeyError, TypeError): pass
        try: self.replyMessage = self.json["extensions"]["replyMessage"]
        except (KeyError, TypeError): pass
        try: self.mediaValue = self.json["mediaValue"]
        except (KeyError, TypeError): pass
        try: self.extensions = self.json["extensions"]
        except (KeyError, TypeError): pass
        try: self.duration = self.json["extensions"]["duration"]
        except (KeyError, TypeError): pass
        try: self.videoDuration = self.json["extensions"]["videoExtensions"]["duration"]
        except (KeyError, TypeError): pass
        try: self.videoHeight = self.json["extensions"]["videoExtensions"]["height"]
        except (KeyError, TypeError): pass
        try: self.videoWidth = self.json["extensions"]["videoExtensions"]["width"]
        except (KeyError, TypeError): pass
        try: self.videoCoverImage = self.json["extensions"]["videoExtensions"]["coverImage"]
        except (KeyError, TypeError): pass
        try: self.originalStickerId = self.json["extensions"]["originalStickerId"]
        except (KeyError, TypeError): pass
        # mentions fixed by enchart
        try: self.mentionUserIds = [m["uid"] for m in self.json["extensions"]["mentionedArray"]]
        except (KeyError, TypeError): pass
        try: self.tippingCoins = self.json["extensions"]["tippingCoins"]
        except (KeyError, TypeError): pass

        return self

class MessageList:
    def __init__(self, data, nextPageToken = None, prevPageToken = None):
        _author, _sticker = [], []

        self.json = data
        self.nextPageToken = nextPageToken
        self.prevPageToken = prevPageToken

        for y in data:
            try: _author.append(y["author"])
            except (KeyError, TypeError): _author.append(None)
            try: _sticker.append(y["extensions"]["sticker"])
            except (KeyError, TypeError): _sticker.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.sticker: StickerList = StickerList(_sticker).StickerList
        self.content = []
        self.includedInSummary = []
        self.isHidden = []
        self.messageType = []
        self.messageId = []
        self.mediaType = []
        self.mediaValue = []
        self.chatBubbleId = []
        self.clientRefId = []
        self.chatId = []
        self.createdTime = []
        self.chatBubbleVersion = []
        self.type = []
        self.extensions = []
        self.mentionUserIds = []
        self.duration = []
        self.originalStickerId = []
        self.videoExtensions = []
        self.videoDuration = []
        self.videoHeight = []
        self.videoWidth = []
        self.videoCoverImage = []
        self.tippingCoins = []

    @property
    def MessageList(self):
        for x in self.json:
            try: self.content.append(x["content"])
            except (KeyError, TypeError): self.content.append(None)
            try: self.includedInSummary.append(x["includedInSummary"])
            except (KeyError, TypeError): self.includedInSummary.append(None)
            try: self.isHidden.append(x["isHidden"])
            except (KeyError, TypeError): self.isHidden.append(None)
            try: self.messageId.append(x["messageId"])
            except (KeyError, TypeError): self.messageId.append(None)
            try: self.chatBubbleId.append(x["chatBubbleId"])
            except (KeyError, TypeError): self.chatBubbleId.append(None)
            try: self.clientRefId.append(x["clientRefId"])
            except (KeyError, TypeError): self.clientRefId.append(None)
            try: self.chatId.append(x["threadId"])
            except (KeyError, TypeError): self.chatId.append(None)
            try: self.messageType.append(x["messageType"])
            except (KeyError, TypeError): self.messageType.append(None)
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)
            try: self.chatBubbleVersion.append(x["chatBubbleVersion"])
            except (KeyError, TypeError): self.chatBubbleVersion.append(None)
            try: self.type.append(x["type"])
            except (KeyError, TypeError): self.type.append(None)
            try: self.mediaValue.append(x["mediaValue"])
            except (KeyError, TypeError): self.mediaValue.append(None)
            try: self.mediaType.append(x["mediaType"])
            except (KeyError, TypeError): self.mediaType.append(None)
            try: self.extensions.append(x["extensions"])
            except (KeyError, TypeError): self.extensions.append(None)
            try: self.duration.append(x["extensions"]["duration"])
            except (KeyError, TypeError): self.duration.append(None)
            try: self.originalStickerId.append(x["extensions"]["originalStickerId"])
            except (KeyError, TypeError): self.originalStickerId.append(None)
            try: self.mentionUserIds.append([m["uid"] for m in x["extensions"]["mentionedArray"]])
            except (KeyError, TypeError): self.mentionUserIds.append(None)
            try: self.videoExtensions.append(x["extensions"]["videoExtensions"])
            except (KeyError, TypeError): self.videoExtensions.append(None)
            try: self.videoDuration.append(x["extensions"]["videoExtensions"]["duration"])
            except (KeyError, TypeError): self.videoDuration.append(None)
            try: self.videoHeight.append(x["extensions"]["videoExtensions"]["height"])
            except (KeyError, TypeError): self.videoHeight.append(None)
            try: self.videoWidth.append(x["extensions"]["videoExtensions"]["width"])
            except (KeyError, TypeError): self.videoWidth.append(None)
            try: self.videoCoverImage.append(x["extensions"]["videoExtensions"]["coverImage"])
            except (KeyError, TypeError): self.videoCoverImage.append(None)
            try: self.tippingCoins.append(x["extensions"]["tippingCoins"])
            except (KeyError, TypeError): self.tippingCoins.append(None)

        return self

class GetMessages:
    def __init__(self, data):
        self.json = data

        self.messageList = []
        self.nextPageToken = None
        self.prevPageToken = None

    @property
    def GetMessages(self):
        try: self.nextPageToken = self.json["paging"]["nextPageToken"]
        except (KeyError, TypeError): pass
        try: self.prevPageToken = self.json["paging"]["prevPageToken"]
        except (KeyError, TypeError): pass
        try: self.messageList = self.json["messageList"]
        except (KeyError, TypeError): pass

        return MessageList(self.messageList, self.nextPageToken, self.prevPageToken).MessageList

class CommunityStickerCollection:
    def __init__(self, data):
        self.json = data

        try: self.sticker: StickerCollectionList = StickerCollectionList(data["stickerCollectionList"]).StickerCollectionList
        except (KeyError, TypeError): self.sticker: StickerCollectionList = StickerCollectionList([])

        self.stickerCollectionCount = None

    @property
    def CommunityStickerCollection(self):
        try: self.stickerCollectionCount = self.json["stickerCollectionCount"]
        except (KeyError, TypeError): pass

        return self

class NotificationList:
    def __init__(self, data):
        _author = []

        self.json = data

        for y in data:
            try: _author.append(y["author"])
            except (KeyError, TypeError): _author.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.contextComId = []
        self.objectText = []
        self.objectType = []
        self.contextValue = []
        self.comId = []
        self.notificationId = []
        self.objectSubtype = []
        self.parentType = []
        self.createdTime = []
        self.parentId = []
        self.type = []
        self.contextText = []
        self.objectId = []
        self.parentText = []

    @property
    def NotificationList(self):
        for x in self.json:
            try: self.parentText.append(x["parentText"])
            except (KeyError, TypeError): self.parentText.append(None)
            try: self.objectId.append(x["objectId"])
            except (KeyError, TypeError): self.objectId.append(None)
            try: self.contextText.append(x["contextText"])
            except (KeyError, TypeError): self.contextText.append(None)
            try: self.type.append(x["type"])
            except (KeyError, TypeError): self.type.append(None)
            try: self.parentId.append(x["parentId"])
            except (KeyError, TypeError): self.parentId.append(None)
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)
            try: self.parentType.append(x["parentType"])
            except (KeyError, TypeError): self.parentType.append(None)
            try: self.objectSubtype.append(x["objectSubtype"])
            except (KeyError, TypeError): self.objectSubtype.append(None)
            try: self.comId.append(x["ndcId"])
            except (KeyError, TypeError): self.comId.append(None)
            try: self.notificationId.append(x["notificationId"])
            except (KeyError, TypeError): self.notificationId.append(None)
            try: self.objectText.append(x["objectText"])
            except (KeyError, TypeError): self.objectText.append(None)
            try: self.contextValue.append(x["contextValue"])
            except (KeyError, TypeError): self.contextValue.append(None)
            try: self.contextComId.append(x["contextNdcId"])
            except (KeyError, TypeError): self.contextComId.append(None)
            try: self.objectType.append(x["objectType"])
            except (KeyError, TypeError): self.objectType.append(None)

        return self

class AdminLogList:
    def __init__(self, data):
        _author = []

        self.json = data

        for y in data:
            try: _author.append(y["author"])
            except (KeyError, TypeError): _author.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.createdTime = []
        self.objectType = []
        self.operationName = []
        self.comId = []
        self.referTicketId = []
        self.extData = []
        self.operationDetail = []
        self.operationLevel = []
        self.moderationLevel = []
        self.operation = []
        self.objectId = []
        self.logId = []
        self.objectUrl = []
        self.content = []
        self.value = []

    @property
    def AdminLogList(self):
        for x in self.json:
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)
            try: self.objectType.append(x["objectType"])
            except (KeyError, TypeError): self.objectType.append(None)
            try: self.operationName.append(x["operationName"])
            except (KeyError, TypeError): self.operationName.append(None)
            try: self.comId.append(x["ndcId"])
            except (KeyError, TypeError): self.comId.append(None)
            try: self.referTicketId.append(x["referTicketId"])
            except (KeyError, TypeError): self.referTicketId.append(None)
            try: self.extData.append(x["extData"])
            except (KeyError, TypeError): self.extData.append(None)
            try: self.content.append(x["extData"]["note"])
            except (KeyError, TypeError): self.content.append(None)
            try: self.value.append(x["extData"]["value"])
            except (KeyError, TypeError): self.value.append(None)
            try: self.operationDetail.append(x["operationDetail"])
            except (KeyError, TypeError): self.operationDetail.append(None)
            try: self.operationLevel.append(x["operationLevel"])
            except (KeyError, TypeError): self.operationLevel.append(None)
            try: self.moderationLevel.append(x["moderationLevel"])
            except (KeyError, TypeError): self.moderationLevel.append(None)
            try: self.operation.append(x["operation"])
            except (KeyError, TypeError): self.operation.append(None)
            try: self.objectId.append(x["objectId"])
            except (KeyError, TypeError): self.objectId.append(None)
            try: self.logId.append(x["logId"])
            except (KeyError, TypeError): self.logId.append(None)
            try: self.objectUrl.append(x["objectUrl"])
            except (KeyError, TypeError): self.objectUrl.append(None)

        return self

class LotteryLog:
    def __init__(self, data):
        self.json = data
        self.awardValue = None
        self.parentId = None
        self.parentType = None
        self.objectId = None
        self.objectType = None
        self.createdTime = None
        self.awardType = None
        self.refObject = None

    @property
    def LotteryLog(self):
        try: self.awardValue = self.json["awardValue"]
        except (KeyError, TypeError): pass
        try: self.parentId = self.json["parentId"]
        except (KeyError, TypeError): pass
        try: self.parentType = self.json["parentType"]
        except (KeyError, TypeError): pass
        try: self.objectId = self.json["objectId"]
        except (KeyError, TypeError): pass
        try: self.objectType = self.json["objectType"]
        except (KeyError, TypeError): pass
        try: self.createdTime = self.json["createdTime"]
        except (KeyError, TypeError): pass
        try: self.awardType = self.json["awardType"]
        except (KeyError, TypeError): pass
        try: self.refObject = self.json["refObject"]
        except (KeyError, TypeError): pass

        return self

class VcReputation:
    def __init__(self, data):
        self.json = data
        self.availableReputation = None
        self.maxReputation = None
        self.reputation = None
        self.participantCount = None
        self.totalReputation = None
        self.duration = None

    @property
    def VcReputation(self):
        try: self.availableReputation = self.json["availableReputation"]
        except (KeyError, TypeError): pass
        try: self.maxReputation = self.json["maxReputation"]
        except (KeyError, TypeError): pass
        try: self.reputation = self.json["reputation"]
        except (KeyError, TypeError): pass
        try: self.participantCount = self.json["participantCount"]
        except (KeyError, TypeError): pass
        try: self.totalReputation = self.json["totalReputation"]
        except (KeyError, TypeError): pass
        try: self.duration = self.json["duration"]
        except (KeyError, TypeError): pass

        return self

class FanClubList:
    __slots__ = (
        "json", "profile", "targetUserProfile", "userId", "lastThankedTime",
        "expiredTime", "createdTime", "status", "targetUserId"
    )

    def __init__(self, data):
        self.json = data

        self.profile = UserProfileList(tuple(y.get("fansUserProfile") for y in data)).UserProfileList
        self.targetUserProfile = UserProfileList(tuple(y.get("targetUserProfile") for y in data)).UserProfileList
        
        self.userId = tuple(x.get("uid") for x in data)
        self.lastThankedTime = tuple(x.get("lastThankedTime") for x in data)
        self.expiredTime = tuple(x.get("expiredTime") for x in data)
        self.createdTime = tuple(x.get("createdTime") for x in data)
        self.status = tuple(x.get("fansStatus") for x in data)
        self.targetUserId = tuple(x.get("targetUid") for x in data)

    @property
    def FanClubList(self):

        return self

class InfluencerFans:
    def __init__(self, data):
        self.json = data

        try: self.influencerProfile: UserProfile = UserProfile(data["influencerUserProfile"]).UserProfile
        except (KeyError, TypeError): self.influencerProfile: UserProfile = UserProfile([])
        try: self.fanClubList: FanClubList = FanClubList(data["fanClubList"]).FanClubList
        except (KeyError, TypeError): self.fanClubList: FanClubList = FanClubList([])

        self.myFanClub = None

    @property
    def InfluencerFans(self):
        try: self.myFanClub = self.json["myFanClub"]
        except (KeyError, TypeError): pass

        return self

class QuizQuestionList:
    def __init__(self, data):
        _answersList = []

        self.json = data

        for y in data:
            try: _answersList.append(QuizAnswers(y["extensions"]["quizQuestionOptList"]).QuizAnswers)
            except (KeyError, TypeError): _answersList.append(None)

        self.status = []
        self.parentType = []
        self.title = []
        self.createdTime = []
        self.questionId = []
        self.parentId = []
        self.mediaList = []
        self.extensions = []
        self.style = []
        self.backgroundImage = []
        self.backgroundColor = []
        self.answerExplanation = []
        self.answersList = _answersList

    @property
    def QuizQuestionList(self):
        for x in self.json:
            try: self.status.append(x["status"])
            except (KeyError, TypeError): self.status.append(None)
            try: self.parentType.append(x["parentType"])
            except (KeyError, TypeError): self.parentType.append(None)
            try: self.title.append(x["title"])
            except (KeyError, TypeError): self.title.append(None)
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)
            try: self.questionId.append(x["quizQuestionId"])
            except (KeyError, TypeError): self.questionId.append(None)
            try: self.parentId.append(x["parentId"])
            except (KeyError, TypeError): self.parentId.append(None)
            try: self.mediaList.append(x["mediaList"])
            except (KeyError, TypeError): self.mediaList.append(None)
            try: self.extensions.append(x["extensions"])
            except (KeyError, TypeError): self.extensions.append(None)
            try: self.style.append(x["extensions"]["style"])
            except (KeyError, TypeError): self.style.append(None)
            try: self.backgroundImage.append(x["extensions"]["style"]["backgroundMediaList"][0][1])
            except (KeyError, TypeError, IndexError): self.backgroundImage.append(None)
            try: self.backgroundColor.append(x["extensions"]["style"]["backgroundColor"])
            except (KeyError, TypeError): self.backgroundColor.append(None)
            try: self.answerExplanation.append(x["extensions"]["quizAnswerExplanation"])
            except (KeyError, TypeError): self.answerExplanation.append(None)

        return self

class QuizAnswers:
    def __init__(self, data):
        self.json = data
        self.answerId = []
        self.isCorrect = []
        self.mediaList = []
        self.title = []
        self.qhash = []

    @property
    def QuizAnswers(self):
        for x in self.json:
            try: self.answerId.append(x["optId"])
            except (KeyError, TypeError): self.answerId.append(None)
            try: self.qhash.append(x["qhash"])
            except (KeyError, TypeError): self.qhash.append(None)
            try: self.isCorrect.append(x["isCorrect"])
            except (KeyError, TypeError): self.isCorrect.append(None)
            try: self.mediaList.append(x["mediaList"])
            except (KeyError, TypeError): self.mediaList.append(None)
            try: self.title.append(x["title"])
            except (KeyError, TypeError): self.title.append(None)

        return self

class QuizRankings:
    def __init__(self, data):
        _rankingList = []

        self.json = data

        for y in data:
            try: _rankingList.append(QuizRanking(y["quizResultRankingList"]).QuizRanking)
            except (KeyError, TypeError): _rankingList.append(None)

        self.rankingList = _rankingList
        self.quizPlayedTimes = None
        self.quizInBestQuizzes = None
        self.profile: QuizRanking = QuizRanking([])

    @property
    def QuizRankings(self):
        try: self.quizPlayedTimes = self.json["quizPlayedTimes"]
        except (KeyError, TypeError): pass
        try: self.quizInBestQuizzes = self.json["quizInBestQuizzes"]
        except (KeyError, TypeError): pass
        try: self.profile: QuizRanking = QuizRanking(self.json["quizResultOfCurrentUser"]).QuizRanking
        except (KeyError, TypeError): pass

        return self

class QuizRanking:
    def __init__(self, data):
        self.json = data
        self.highestMode = None
        self.modifiedTime = None
        self.isFinished = None
        self.hellIsFinished = None
        self.highestScore = None
        self.beatRate = None
        self.lastBeatRate = None
        self.totalTimes = None
        self.latestScore = None
        self.latestMode = None
        self.createdTime = None

    @property
    def QuizRanking(self):
        try: self.highestMode = self.json["highestMode"]
        except (KeyError, TypeError): pass
        try: self.modifiedTime = self.json["modifiedTime"]
        except (KeyError, TypeError): pass
        try: self.isFinished = self.json["isFinished"]
        except (KeyError, TypeError): pass
        try: self.hellIsFinished = self.json["hellIsFinished"]
        except (KeyError, TypeError): pass
        try: self.highestScore = self.json["highestScore"]
        except (KeyError, TypeError): pass
        try: self.beatRate = self.json["beatRate"]
        except (KeyError, TypeError): pass
        try: self.lastBeatRate = self.json["lastBeatRate"]
        except (KeyError, TypeError): pass
        try: self.totalTimes = self.json["totalTimes"]
        except (KeyError, TypeError): pass
        try: self.latestScore = self.json["latestScore"]
        except (KeyError, TypeError): pass
        try: self.latestMode = self.json["latestMode"]
        except (KeyError, TypeError): pass
        try: self.createdTime = self.json["createdTime"]
        except (KeyError, TypeError): pass

        return self

class QuizRankingList:
    def __init__(self, data):
        _author = []

        self.json = data

        for y in data:
            try: _author.append(y["author"])
            except (KeyError, TypeError): _author.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.highestMode = []
        self.modifiedTime = []
        self.isFinished = []
        self.hellIsFinished = []
        self.highestScore = []
        self.beatRate = []
        self.lastBeatRate = []
        self.totalTimes = []
        self.latestScore = []
        self.latestMode = []
        self.createdTime = []

    @property
    def QuizRankingList(self):
        for x in self.json:
            try: self.highestMode.append(x["highestMode"])
            except (KeyError, TypeError): self.highestMode.append(None)
            try: self.modifiedTime.append(x["modifiedTime"])
            except (KeyError, TypeError): self.modifiedTime.append(None)
            try: self.isFinished.append(x["isFinished"])
            except (KeyError, TypeError): self.isFinished.append(None)
            try: self.hellIsFinished.append(x["hellIsFinished"])
            except (KeyError, TypeError): self.hellIsFinished.append(None)
            try: self.highestScore.append(x["highestScore"])
            except (KeyError, TypeError): self.highestScore.append(None)
            try: self.beatRate.append(x["beatRate"])
            except (KeyError, TypeError): self.beatRate.append(None)
            try: self.lastBeatRate.append(x["lastBeatRate"])
            except (KeyError, TypeError): self.lastBeatRate.append(None)
            try: self.totalTimes.append(x["totalTimes"])
            except (KeyError, TypeError): self.totalTimes.append(None)
            try: self.latestScore.append(x["latestScore"])
            except (KeyError, TypeError): self.latestScore.append(None)
            try: self.latestMode.append(x["latestMode"])
            except (KeyError, TypeError): self.latestMode.append(None)
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)

        return self

class SharedFolderFile:
    def __init__(self, data):
        self.json = data

        try: self.author: UserProfile = UserProfile(data["author"]).UserProfile
        except (KeyError, TypeError): self.author: UserProfile = UserProfile([])

        self.votesCount = None
        self.createdTime = None
        self.modifiedTime = None
        self.extensions = None
        self.title = None
        self.media = None
        self.width = None
        self.height = None
        self.commentsCount = None
        self.fileType = None
        self.votedValue = None
        self.fileId = None
        self.comId = None
        self.status = None
        self.fileUrl = None
        self.mediaType = None

    @property
    def SharedFolderFile(self):
        try: self.votesCount = self.json["votesCount"]
        except (KeyError, TypeError): pass
        try: self.createdTime = self.json["createdTime"]
        except (KeyError, TypeError): pass
        try: self.modifiedTime = self.json["modifiedTime"]
        except (KeyError, TypeError): pass
        try: self.extensions = self.json["extensions"]
        except (KeyError, TypeError): pass
        try: self.width = self.json["width_hq"]
        except (KeyError, TypeError): pass
        try: self.height = self.json["height_hq"]
        except (KeyError, TypeError): pass
        try: self.title = self.json["title"]
        except (KeyError, TypeError): pass
        try: self.media = self.json["media"]
        except (KeyError, TypeError): pass
        try: self.mediaType = self.json["media"][0]
        except (KeyError, TypeError): pass
        try: self.fileUrl = self.json["media"][1]
        except (KeyError, TypeError, IndexError): pass
        try: self.commentsCount = self.json["commentsCount"]
        except (KeyError, TypeError): pass
        try: self.fileType = self.json["fileType"]
        except (KeyError, TypeError): pass
        try: self.votedValue = self.json["votedValue"]
        except (KeyError, TypeError): pass
        try: self.fileId = self.json["fileId"]
        except (KeyError, TypeError): pass
        try: self.comId = self.json["ndcId"]
        except (KeyError, TypeError): pass
        try: self.status = self.json["status"]
        except (KeyError, TypeError): pass

        return self

class SharedFolderFileList:
    def __init__(self, data):
        _author = []

        self.json = data

        for y in data:
            try: _author.append(y["author"])
            except (KeyError, TypeError): _author.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.votesCount = []
        self.createdTime = []
        self.modifiedTime = []
        self.extensions = []
        self.title = []
        self.media = []
        self.width = []
        self.height = []
        self.commentsCount = []
        self.fileType = []
        self.votedValue = []
        self.fileId = []
        self.comId = []
        self.status = []
        self.fileUrl = []
        self.mediaType = []

    @property
    def SharedFolderFileList(self):
        for x in self.json:
            try: self.votesCount.append(x["votesCount"])
            except (KeyError, TypeError): self.votesCount.append(None)
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)
            try: self.modifiedTime.append(x["modifiedTime"])
            except (KeyError, TypeError): self.modifiedTime.append(None)
            try: self.extensions.append(x["extensions"])
            except (KeyError, TypeError): self.extensions.append(None)
            try: self.width.append(x["width_hq"])
            except (KeyError, TypeError): self.width.append(None)
            try: self.height.append(x["height_hq"])
            except (KeyError, TypeError): self.height.append(None)
            try: self.title.append(x["title"])
            except (KeyError, TypeError): self.title.append(None)
            try: self.media.append(x["media"])
            except (KeyError, TypeError): self.media.append(None)
            try: self.mediaType.append(x["media"][0])
            except (KeyError, TypeError): self.mediaType.append(None)
            try: self.fileUrl.append(x["media"][1])
            except (KeyError, TypeError, IndexError): self.fileUrl.append(None)
            try: self.commentsCount.append(x["commentsCount"])
            except (KeyError, TypeError): self.commentsCount.append(None)
            try: self.fileType.append(x["fileType"])
            except (KeyError, TypeError): self.fileType.append(None)
            try: self.votedValue.append(x["votedValue"])
            except (KeyError, TypeError): self.votedValue.append(None)
            try: self.fileId.append(x["fileId"])
            except (KeyError, TypeError): self.fileId.append(None)
            try: self.comId.append(x["ndcId"])
            except (KeyError, TypeError): self.comId.append(None)
            try: self.status.append(x["status"])
            except (KeyError, TypeError): self.status.append(None)

        return self

class Event:
    def __init__(self, data):
        self.json = data
        self.comId = None
        self.alertOption = None
        self.membershipStatus = None
        self.actions = None
        self.target = None
        self.params = None
        self.threadType = None
        self.id = None
        self.duration = None

        try: self.message: Message = Message(data["chatMessage"]).Message
        except (KeyError, TypeError): self.message: Message = Message([])

    @property
    def Event(self):
        try: self.comId = self.json["ndcId"]
        except (KeyError, TypeError): pass
        try: self.alertOption = self.json["alertOption"]
        except (KeyError, TypeError): pass
        try: self.membershipStatus = self.json["membershipStatus"]
        except (KeyError, TypeError): pass
        try: self.actions = self.json["actions"]
        except (KeyError, TypeError): pass
        try: self.target = self.json["target"]
        except (KeyError, TypeError): pass
        try: self.params = self.json["params"]
        except (KeyError, TypeError): pass
        try: self.threadType = self.json["params"]["threadType"]
        except (KeyError, TypeError): pass
        try: self.duration = self.json["params"]["duration"]
        except (KeyError, TypeError): pass
        try: self.id = self.json["id"]
        except (KeyError, TypeError): pass

        return self

class JoinRequest:
    def __init__(self, data):
        _author = []

        self.json = data

        for y in data["communityMembershipRequestList"]:
            try: _author.append(y)
            except (KeyError, TypeError): _author.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.communityMembershipRequestCount = None

    @property
    def JoinRequest(self):
        try: self.communityMembershipRequestCount = self.json["communityMembershipRequestCount"]
        except (KeyError, TypeError): pass

        return self

class CommunityStats:
    def __init__(self, data):
        self.json = data
        self.dailyActiveMembers = None
        self.monthlyActiveMembers = None
        self.totalTimeSpent = None
        self.totalPostsCreated = None
        self.newMembersToday = None
        self.totalMembers = None

    @property
    def CommunityStats(self):
        try: self.dailyActiveMembers = self.json["dailyActiveMembers"]
        except (KeyError, TypeError): pass
        try: self.monthlyActiveMembers = self.json["monthlyActiveMembers"]
        except (KeyError, TypeError): pass
        try: self.totalTimeSpent = self.json["totalTimeSpent"]
        except (KeyError, TypeError): pass
        try: self.totalPostsCreated = self.json["totalPostsCreated"]
        except (KeyError, TypeError): pass
        try: self.newMembersToday = self.json["newMembersToday"]
        except (KeyError, TypeError): pass
        try: self.totalMembers = self.json["totalMembers"]
        except (KeyError, TypeError): pass

        return self


class InviteCode:
    def __init__(self, data):
        self.json = data

        try: self.author: UserProfile = UserProfile(data["author"]).UserProfile
        except (KeyError, TypeError): self.author: UserProfile = UserProfile([])

        self.status = None
        self.duration = None
        self.invitationId = None
        self.link = None
        self.modifiedTime = None
        self.comId = None
        self.createdTime = None
        self.inviteCode = None

    @property
    def InviteCode(self):
        try: self.status = self.json["status"]
        except (KeyError, TypeError): pass
        try: self.duration = self.json["duration"]
        except (KeyError, TypeError): pass
        try: self.invitationId = self.json["invitationId"]
        except (KeyError, TypeError): pass
        try: self.link = self.json["link"]
        except (KeyError, TypeError): pass
        try: self.modifiedTime = self.json["modifiedTime"]
        except (KeyError, TypeError): pass
        try: self.comId = self.json["ndcId"]
        except (KeyError, TypeError): pass
        try: self.createdTime = self.json["createdTime"]
        except (KeyError, TypeError): pass
        try: self.inviteCode = self.json["inviteCode"]
        except (KeyError, TypeError): pass

        return self


class InviteCodeList:
    def __init__(self, data):
        _author = []

        self.json = data

        for y in data:
            try: _author.append(y["author"])
            except (KeyError, TypeError): _author.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.status = []
        self.duration = []
        self.invitationId = []
        self.link = []
        self.modifiedTime = []
        self.comId = []
        self.createdTime = []
        self.inviteCode = []

    @property
    def InviteCodeList(self):
        for x in self.json:
            try: self.status.append(x["status"])
            except (KeyError, TypeError): self.status.append(None)
            try: self.duration.append(x["duration"])
            except (KeyError, TypeError): self.duration.append(None)
            try: self.invitationId.append(x["invitationId"])
            except (KeyError, TypeError): self.invitationId.append(None)
            try: self.link.append(x["link"])
            except (KeyError, TypeError): self.link.append(None)
            try: self.modifiedTime.append(x["modifiedTime"])
            except (KeyError, TypeError): self.modifiedTime.append(None)
            try: self.comId.append(x["ndcId"])
            except (KeyError, TypeError): self.comId.append(None)
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)
            try: self.inviteCode.append(x["inviteCode"])
            except (KeyError, TypeError): self.inviteCode.append(None)

        return self

class WikiRequestList:
    def __init__(self, data):
        _author, _wiki, _originalWiki = [], [], []

        self.json = data

        for y in data:
            try: _author.append(y["operator"])
            except (KeyError, TypeError): _author.append(None)
            try: _wiki.append(y["item"])
            except (KeyError, TypeError): _wiki.append(None)
            try: _originalWiki.append(y["originalItem"])
            except (KeyError, TypeError): _originalWiki.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.wiki: WikiList = WikiList(_wiki).WikiList
        self.originalWiki: WikiList = WikiList(_originalWiki).WikiList

        self.authorId = []
        self.status = []
        self.modifiedTime = []
        self.message = []
        self.wikiId = []
        self.requestId = []
        self.destinationItemId = []
        self.createdTime = []
        self.responseMessage = []

    @property
    def WikiRequestList(self):
        for x in self.json:
            try: self.authorId.append(x["uid"])
            except (KeyError, TypeError): self.authorId.append(None)
            try: self.status.append(x["status"])
            except (KeyError, TypeError): self.status.append(None)
            try: self.modifiedTime.append(x["modifiedTime"])
            except (KeyError, TypeError): self.modifiedTime.append(None)
            try: self.message.append(x["message"])
            except (KeyError, TypeError): self.message.append(None)
            try: self.wikiId.append(x["itemId"])
            except (KeyError, TypeError): self.wikiId.append(None)
            try: self.requestId.append(x["requestId"])
            except (KeyError, TypeError): self.requestId.append(None)
            try: self.destinationItemId.append(x["destinationItemId"])
            except (KeyError, TypeError): self.destinationItemId.append(None)
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)
            try: self.responseMessage.append(x["responseMessage"])
            except (KeyError, TypeError): self.responseMessage.append(None)

        return self

class NoticeList:
    def __init__(self, data):
        _author, _targetUser = [], []

        self.json = data

        for y in data:
            try: _author.append(y["operator"])
            except (KeyError, TypeError): _author.append(None)
            try: _targetUser.append(y["targetUser"])
            except (KeyError, TypeError): _targetUser.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.targetUser: UserProfileList = UserProfileList(_targetUser).UserProfileList

        self.title = []
        self.icon = []
        self.noticeId = []
        self.status = []
        self.comId = []
        self.modifiedTime = []
        self.createdTime = []
        self.extensions = []
        self.content = []
        self.community = []
        self.type = []
        self.notificationId = []
        self.authorId = []
        self.style = []
        self.backgroundColor = []
        self.config = []
        self.showCommunity = []
        self.showAuthor = []
        self.allowQuickOperation = []
        self.operationList = []

    @property
    def NoticeList(self):
        for x in self.json:
            try: self.title.append(x["title"])
            except (KeyError, TypeError): self.title.append(None)
            try: self.icon.append(x["icon"])
            except (KeyError, TypeError): self.icon.append(None)
            try: self.noticeId.append(x["noticeId"])
            except (KeyError, TypeError): self.noticeId.append(None)
            try: self.status.append(x["status"])
            except (KeyError, TypeError): self.status.append(None)
            try: self.comId.append(x["ndcId"])
            except (KeyError, TypeError): self.comId.append(None)
            try: self.modifiedTime.append(x["modifiedTime"])
            except (KeyError, TypeError): self.modifiedTime.append(None)
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)
            try: self.extensions.append(x["extensions"])
            except (KeyError, TypeError): self.extensions.append(None)
            try: self.authorId.append(x["extensions"]["operatorUid"])
            except (KeyError, TypeError): self.authorId.append(None)
            try: self.config.append(x["extensions"]["config"])
            except (KeyError, TypeError): self.config.append(None)
            try: self.showCommunity.append(x["extensions"]["config"]["showCommunity"])
            except (KeyError, TypeError): self.showCommunity.append(None)
            try: self.showAuthor.append(x["extensions"]["config"]["showOperator"])
            except (KeyError, TypeError): self.showAuthor.append(None)
            try: self.allowQuickOperation.append(x["extensions"]["config"]["allowQuickOperation"])
            except (KeyError, TypeError): self.allowQuickOperation.append(None)
            try: self.operationList.append(x["extensions"]["config"]["operationList"])
            except (KeyError, TypeError): self.operationList.append(None)
            try: self.style.append(x["extensions"]["style"])
            except (KeyError, TypeError): self.style.append(None)
            try: self.backgroundColor.append(x["extensions"]["style"]["backgroundColor"])
            except (KeyError, TypeError): self.backgroundColor.append(None)
            try: self.content.append(x["content"])
            except (KeyError, TypeError): self.content.append(None)
            try: self.community.append(x["community"])
            except (KeyError, TypeError): self.community.append(None)
            try: self.type.append(x["type"])
            except (KeyError, TypeError): self.type.append(None)
            try: self.notificationId.append(x["notificationId"])
            except (KeyError, TypeError): self.notificationId.append(None)

        return self


class LiveLayer:
    def __init__(self, data):
        self.json = data

        self.userProfileCount = []
        self.topic = []
        self.userProfileList = []
        self.mediaList = []

    @property
    def LiveLayer(self):
        for x in self.json:
            try: self.userProfileCount.append(x["userProfileCount"])
            except (KeyError, TypeError): self.userProfileCount.append(None)
            try: self.topic.append(x["topic"])
            except (KeyError, TypeError): self.topic.append(None)
            try: self.userProfileList.append(UserProfileList(x["userProfileList"]).UserProfileList)
            except (KeyError, TypeError): self.userProfileList.append(None)
            try: self.mediaList.append(x["mediaList"])
            except (KeyError, TypeError): self.mediaList.append(None)

        return self


class AvatarFrameList:
    def __init__(self, data):
        _author, _targetUser = [], []

        self.json = data

        for y in data:
            try: _author.append(y["operator"])
            except (KeyError, TypeError): _author.append(None)
            try: _targetUser.append(y["targetUser"])
            except (KeyError, TypeError): _targetUser.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.targetUser: UserProfileList = UserProfileList(_targetUser).UserProfileList

        self.isGloballyAvailable = []
        self.extensions = []
        self.frameType = []
        self.resourceUrl = []
        self.md5 = []
        self.icon = []
        self.createdTime = []
        self.config = []
        self.moodColor = []
        self.configName = []
        self.configVersion = []
        self.userIconBorderColor = []
        self.avatarFramePath = []
        self.avatarId = []
        self.ownershipStatus = []
        self.frameUrl = []
        self.additionalBenefits = []
        self.firstMonthFreeAminoPlusMembership = []
        self.restrictionInfo = []
        self.ownerType = []
        self.restrictType = []
        self.restrictValue = []
        self.availableDuration = []
        self.discountValue = []
        self.discountStatus = []
        self.ownerId = []
        self.ownershipInfo = []
        self.isAutoRenew = []
        self.modifiedTime = []
        self.name = []
        self.frameId = []
        self.version = []
        self.isNew = []
        self.availableComIds = []
        self.status = []

    @property
    def AvatarFrameList(self):
        for x in self.json:
            try: self.isGloballyAvailable.append(x["isGloballyAvailable"])
            except (KeyError, TypeError): self.isGloballyAvailable.append(None)
            try: self.extensions.append(x["extensions"])
            except (KeyError, TypeError): self.extensions.append(None)
            try: self.frameType.append(x["frameType"])
            except (KeyError, TypeError): self.frameType.append(None)
            try: self.resourceUrl.append(x["resourceUrl"])
            except (KeyError, TypeError): self.resourceUrl.append(None)
            try: self.md5.append(x["md5"])
            except (KeyError, TypeError): self.md5.append(None)
            try: self.icon.append(x["icon"])
            except (KeyError, TypeError): self.icon.append(None)
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)
            try: self.config.append(x["config"])
            except (KeyError, TypeError): self.config.append(None)
            try: self.moodColor.append(x["config"]["moodColor"])
            except (KeyError, TypeError): self.moodColor.append(None)
            try: self.configName.append(x["config"]["name"])
            except (KeyError, TypeError): self.configName.append(None)
            try: self.configVersion.append(x["config"]["version"])
            except (KeyError, TypeError): self.configVersion.append(None)
            try: self.userIconBorderColor.append(x["config"]["userIconBorderColor"])
            except (KeyError, TypeError): self.userIconBorderColor.append(None)
            try: self.avatarFramePath.append(x["config"]["avatarFramePath"])
            except (KeyError, TypeError): self.avatarFramePath.append(None)
            try: self.avatarId.append(x["config"]["id"])
            except (KeyError, TypeError): self.avatarId.append(None)
            try: self.ownershipStatus.append(x["ownershipStatus"])
            except (KeyError, TypeError): self.ownershipStatus.append(None)
            try: self.frameUrl.append(x["frameUrl"])
            except (KeyError, TypeError): self.frameUrl.append(None)
            try: self.additionalBenefits.append(x["additionalBenefits"])
            except (KeyError, TypeError): self.additionalBenefits.append(None)
            try: self.firstMonthFreeAminoPlusMembership.append(x["additionalBenefits"]["firstMonthFreeAminoPlusMembership"])
            except (KeyError, TypeError): self.firstMonthFreeAminoPlusMembership.append(None)
            try: self.restrictionInfo.append(x["restrictionInfo"])
            except (KeyError, TypeError): self.restrictionInfo.append(None)
            try: self.ownerType.append(x["restrictionInfo"]["ownerType"])
            except (KeyError, TypeError): self.ownerType.append(None)
            try: self.restrictType.append(x["restrictionInfo"]["restrictType"])
            except (KeyError, TypeError): self.restrictType.append(None)
            try: self.restrictValue.append(x["restrictionInfo"]["restrictValue"])
            except (KeyError, TypeError): self.restrictValue.append(None)
            try: self.availableDuration.append(x["restrictionInfo"]["availableDuration"])
            except (KeyError, TypeError): self.availableDuration.append(None)
            try: self.discountValue.append(x["restrictionInfo"]["discountValue"])
            except (KeyError, TypeError): self.discountValue.append(None)
            try: self.discountStatus.append(x["restrictionInfo"]["discountStatus"])
            except (KeyError, TypeError): self.discountStatus.append(None)
            try: self.ownerId.append(x["restrictionInfo"]["ownerUid"])
            except (KeyError, TypeError): self.ownerId.append(None)
            try: self.ownershipInfo.append(x["ownershipInfo"])
            except (KeyError, TypeError): self.ownershipInfo.append(None)
            try: self.isAutoRenew.append(x["ownershipInfo"]["isAutoRenew"])
            except (KeyError, TypeError): self.isAutoRenew.append(None)
            try: self.name.append(x["name"])
            except (KeyError, TypeError): self.name.append(None)
            try: self.modifiedTime.append(x["modifiedTime"])
            except (KeyError, TypeError): self.modifiedTime.append(None)
            try: self.frameId.append(x["frameId"])
            except (KeyError, TypeError): self.frameId.append(None)
            try: self.version.append(x["version"])
            except (KeyError, TypeError): self.version.append(None)
            try: self.isNew.append(x["isNew"])
            except (KeyError, TypeError): self.isNew.append(None)
            try: self.status.append(x["status"])
            except (KeyError, TypeError): self.status.append(None)
            try: self.availableComIds.append(x["availableNdcIds"])
            except (KeyError, TypeError): self.availableComIds.append(None)

        return self


class BubbleConfig:
    def __init__(self, data):
        self.json = data
        self.status = None
        self.allowedSlots = None
        self.name = None
        self.vertexInset = None
        self.zoomPoint = None
        self.coverImage = None
        self.bubbleType = None
        self.contentInsets = None
        self.version = None
        self.linkColor = None
        self.backgroundPath = None
        self.id = None
        self.previewBackgroundUrl = None

    @property
    def BubbleConfig(self):
        try: self.status = self.json["status"]
        except (KeyError, TypeError): pass
        try: self.allowedSlots = self.json["allowedSlots"]
        except (KeyError, TypeError): pass
        try: self.name = self.json["name"]
        except (KeyError, TypeError): pass
        try: self.vertexInset = self.json["vertexInset"]
        except (KeyError, TypeError): pass
        try: self.zoomPoint = self.json["zoomPoint"]
        except (KeyError, TypeError): pass
        try: self.coverImage = self.json["coverImage"]
        except (KeyError, TypeError): pass
        try: self.bubbleType = self.json["bubbleType"]
        except (KeyError, TypeError): pass
        try: self.contentInsets = self.json["contentInsets"]
        except (KeyError, TypeError): pass
        try: self.version = self.json["version"]
        except (KeyError, TypeError): pass
        try: self.linkColor = self.json["linkColor"]
        except (KeyError, TypeError): pass
        try: self.backgroundPath = self.json["backgroundPath"]
        except (KeyError, TypeError): pass
        try: self.id = self.json["id"]
        except (KeyError, TypeError): pass
        try: self.previewBackgroundUrl = self.json["previewBackgroundUrl"]
        except (KeyError, TypeError): pass

        return self


class Bubble:
    def __init__(self, data):
        try: self.config: BubbleConfig = BubbleConfig(data["config"])
        except (KeyError, TypeError): self.config: BubbleConfig = BubbleConfig([])

        self.json = data
        self.uid = None
        self.isActivated = None
        self.isNew = None
        self.bubbleId = None
        self.resourceUrl = None
        self.version = None
        self.backgroundImage = None
        self.status = None
        self.modifiedTime = None
        self.ownershipInfo = None
        self.expiredTime = None
        self.isAutoRenew = None
        self.ownershipStatus = None
        self.bannerImage = None
        self.md5 = None
        self.name = None
        self.coverImage = None
        self.bubbleType = None
        self.extensions = None
        self.templateId = None
        self.createdTime = None
        self.deletable = None
        self.backgroundMedia = None
        self.description = None
        self.materialUrl = None
        self.comId = None
        self.restrictionInfo = None
        self.discountValue = None
        self.discountStatus = None
        self.ownerId = None
        self.ownerType = None
        self.restrictType = None
        self.restrictValue = None
        self.availableDuration = None

    @property
    def Bubble(self):
        try: self.uid = self.json["uid"]
        except (KeyError, TypeError): pass
        try: self.isActivated = self.json["isActivated"]
        except (KeyError, TypeError): pass
        try: self.isNew = self.json["isNew"]
        except (KeyError, TypeError): pass
        try: self.bubbleId = self.json["bubbleId"]
        except (KeyError, TypeError): pass
        try: self.resourceUrl = self.json["resourceUrl"]
        except (KeyError, TypeError): pass
        try: self.backgroundImage = self.json["backgroundImage"]
        except (KeyError, TypeError): pass
        try: self.status = self.json["status"]
        except (KeyError, TypeError): pass
        try: self.modifiedTime = self.json["modifiedTime"]
        except (KeyError, TypeError): pass
        try: self.ownershipInfo = self.json["ownershipInfo"]
        except (KeyError, TypeError): pass
        try: self.expiredTime = self.json["ownershipInfo"]["expiredTime"]
        except (KeyError, TypeError): pass
        try: self.isAutoRenew = self.json["ownershipInfo"]["isAutoRenew"]
        except (KeyError, TypeError): pass
        try: self.ownershipStatus = self.json["ownershipStatus"]
        except (KeyError, TypeError): pass
        try: self.bannerImage = self.json["bannerImage"]
        except (KeyError, TypeError): pass
        try: self.md5 = self.json["md5"]
        except (KeyError, TypeError): pass
        try: self.name = self.json["name"]
        except (KeyError, TypeError): pass
        try: self.coverImage = self.json["coverImage"]
        except (KeyError, TypeError): pass
        try: self.bubbleType = self.json["bubbleType"]
        except (KeyError, TypeError): pass
        try: self.extensions = self.json["extensions"]
        except (KeyError, TypeError): pass
        try: self.templateId = self.json["templateId"]
        except (KeyError, TypeError): pass
        try: self.createdTime = self.json["createdTime"]
        except (KeyError, TypeError): pass
        try: self.deletable = self.json["deletable"]
        except (KeyError, TypeError): pass
        try: self.backgroundMedia = self.json["backgroundMedia"]
        except (KeyError, TypeError): pass
        try: self.description = self.json["description"]
        except (KeyError, TypeError): pass
        try: self.materialUrl = self.json["materialUrl"]
        except (KeyError, TypeError): pass
        try: self.comId = self.json["ndcId"]
        except (KeyError, TypeError): pass
        try: self.restrictionInfo = self.json["restrictionInfo"]
        except (KeyError, TypeError): pass
        try: self.discountStatus = self.json["restrictionInfo"]["discountStatus"]
        except (KeyError, TypeError): pass
        try: self.discountValue = self.json["restrictionInfo"]["discountValue"]
        except (KeyError, TypeError): pass
        try: self.ownerId = self.json["restrictionInfo"]["ownerUid"]
        except (KeyError, TypeError): pass
        try: self.ownerType = self.json["restrictionInfo"]["ownerType"]
        except (KeyError, TypeError): pass
        try: self.restrictType = self.json["restrictionInfo"]["restrictType"]
        except (KeyError, TypeError): pass
        try: self.restrictValue = self.json["restrictionInfo"]["restrictValue"]
        except (KeyError, TypeError): pass
        try: self.availableDuration = self.json["restrictionInfo"]["availableDuration"]
        except (KeyError, TypeError): pass

        return self


class BubbleConfigList:
    def __init__(self, data):
        self.json = data
        self.status = []
        self.allowedSlots = []
        self.name = []
        self.vertexInset = []
        self.zoomPoint = []
        self.coverImage = []
        self.bubbleType = []
        self.contentInsets = []
        self.version = []
        self.linkColor = []
        self.backgroundPath = []
        self.id = []
        self.previewBackgroundUrl = []

    @property
    def BubbleConfigList(self):
        for x in self.json:
            try: self.status.append(x["status"])
            except (KeyError, TypeError): self.status.append(None)
            try: self.allowedSlots.append(x["allowedSlots"])
            except (KeyError, TypeError): self.allowedSlots.append(None)
            try: self.name.append(x["name"])
            except (KeyError, TypeError): self.name.append(None)
            try: self.vertexInset.append(x["vertexInset"])
            except (KeyError, TypeError): self.vertexInset.append(None)
            try: self.zoomPoint.append(x["zoomPoint"])
            except (KeyError, TypeError): self.zoomPoint.append(None)
            try: self.coverImage.append(x["coverImage"])
            except (KeyError, TypeError): self.coverImage.append(None)
            try: self.bubbleType.append(x["bubbleType"])
            except (KeyError, TypeError): self.bubbleType.append(None)
            try: self.contentInsets.append(x["contentInsets"])
            except (KeyError, TypeError): self.contentInsets.append(None)
            try: self.version.append(x["version"])
            except (KeyError, TypeError): self.version.append(None)
            try: self.linkColor.append(x["linkColor"])
            except (KeyError, TypeError): self.linkColor.append(None)
            try: self.backgroundPath.append(x["backgroundPath"])
            except (KeyError, TypeError): self.backgroundPath.append(None)
            try: self.id.append(x["id"])
            except (KeyError, TypeError): self.id.append(None)
            try: self.previewBackgroundUrl.append(x["previewBackgroundUrl"])
            except (KeyError, TypeError): self.previewBackgroundUrl.append(None)

        return self

class BubbleList:
    def __init__(self, data):
        _config = []

        self.json = data

        for y in data:
            try: _config.append(y["config"])
            except (KeyError, TypeError): _config.append(None)

        self.config: BubbleConfigList = BubbleConfigList(_config).BubbleConfigList
        self.uid = []
        self.isActivated = []
        self.isNew = []
        self.bubbleId = []
        self.resourceUrl = []
        self.version = []
        self.backgroundImage = []
        self.status = []
        self.modifiedTime = []
        self.ownershipInfo = []
        self.expiredTime = []
        self.isAutoRenew = []
        self.ownershipStatus = []
        self.bannerImage = []
        self.md5 = []
        self.name = []
        self.coverImage = []
        self.bubbleType = []
        self.extensions = []
        self.templateId = []
        self.createdTime = []
        self.deletable = []
        self.backgroundMedia = []
        self.description = []
        self.materialUrl = []
        self.comId = []
        self.restrictionInfo = []
        self.discountValue = []
        self.discountStatus = []
        self.ownerId = []
        self.ownerType = []
        self.restrictType = []
        self.restrictValue = []
        self.availableDuration = []

    @property
    def BubbleList(self):
        for x in self.json:
            try: self.uid.append(x["uid"])
            except (KeyError, TypeError): self.uid.append(None)
            try: self.isActivated.append(x["isActivated"])
            except (KeyError, TypeError): self.isActivated.append(None)
            try: self.isNew.append(x["isNew"])
            except (KeyError, TypeError): self.isNew.append(None)
            try: self.bubbleId.append(x["bubbleId"])
            except (KeyError, TypeError): self.bubbleId.append(None)
            try: self.resourceUrl.append(x["resourceUrl"])
            except (KeyError, TypeError): self.resourceUrl.append(None)
            try: self.backgroundImage.append(x["backgroundImage"])
            except (KeyError, TypeError): self.backgroundImage.append(None)
            try: self.status.append(x["status"])
            except (KeyError, TypeError): self.status.append(None)
            try: self.modifiedTime.append(x["modifiedTime"])
            except (KeyError, TypeError): self.modifiedTime.append(None)
            try: self.ownershipInfo.append(x["ownershipInfo"])
            except (KeyError, TypeError): self.ownershipInfo.append(None)
            try: self.expiredTime.append(x["ownershipInfo"]["expiredTime"])
            except (KeyError, TypeError): self.expiredTime.append(None)
            try: self.isAutoRenew.append(x["ownershipInfo"]["isAutoRenew"])
            except (KeyError, TypeError): self.isAutoRenew.append(None)
            try: self.ownershipStatus.append(x["ownershipStatus"])
            except (KeyError, TypeError): self.ownershipStatus.append(None)
            try: self.bannerImage.append(x["bannerImage"])
            except (KeyError, TypeError): self.bannerImage.append(None)
            try: self.md5.append(x["md5"])
            except (KeyError, TypeError): self.md5.append(None)
            try: self.name.append(x["name"])
            except (KeyError, TypeError): self.name.append(None)
            try: self.coverImage.append(x["coverImage"])
            except (KeyError, TypeError): self.coverImage.append(None)
            try: self.bubbleType.append(x["bubbleType"])
            except (KeyError, TypeError): self.bubbleType.append(None)
            try: self.extensions.append(x["extensions"])
            except (KeyError, TypeError): self.extensions.append(None)
            try: self.templateId.append(x["templateId"])
            except (KeyError, TypeError): self.templateId.append(None)
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)
            try: self.deletable.append(x["deletable"])
            except (KeyError, TypeError): self.deletable.append(None)
            try: self.backgroundMedia.append(x["backgroundMedia"])
            except (KeyError, TypeError): self.backgroundMedia.append(None)
            try: self.description.append(x["description"])
            except (KeyError, TypeError): self.description.append(None)
            try: self.materialUrl.append(x["materialUrl"])
            except (KeyError, TypeError): self.materialUrl.append(None)
            try: self.comId.append(x["ndcId"])
            except (KeyError, TypeError): self.comId.append(None)
            try: self.restrictionInfo.append(x["restrictionInfo"])
            except (KeyError, TypeError): self.restrictionInfo.append(None)
            try: self.discountStatus.append(x["restrictionInfo"]["discountStatus"])
            except (KeyError, TypeError): self.discountStatus.append(None)
            try: self.discountValue.append(x["restrictionInfo"]["discountValue"])
            except (KeyError, TypeError): self.discountValue.append(None)
            try: self.ownerId.append(x["restrictionInfo"]["ownerUid"])
            except (KeyError, TypeError): self.ownerId.append(None)
            try: self.ownerType.append(x["restrictionInfo"]["ownerType"])
            except (KeyError, TypeError): self.ownerType.append(None)
            try: self.restrictType.append(x["restrictionInfo"]["restrictType"])
            except (KeyError, TypeError): self.restrictType.append(None)
            try: self.restrictValue.append(x["restrictionInfo"]["restrictValue"])
            except (KeyError, TypeError): self.restrictValue.append(None)
            try: self.availableDuration.append(x["restrictionInfo"]["availableDuration"])
            except (KeyError, TypeError): self.availableDuration.append(None)

        return self

class AvatarFrame:
    def __init__(self, data):
        self.json = data

        self.name = []
        self.id = []
        self.resourceUrl = []
        self.icon = []
        self.frameUrl = []
        self.value = []

    @property
    def AvatarFrame(self):
        for x in self.json:
            try: self.name.append(x["refObject"]["config"]["name"])
            except (KeyError, TypeError): self.name.append(None)
            try: self.id.append(x["refObject"]["config"]["id"])
            except (KeyError, TypeError): self.id.append(None)
            try: self.resourceUrl.append(x["refObject"]["resourceUrl"])
            except (KeyError, TypeError): self.resourceUrl.append(None)
            try: self.icon.append(x["refObject"]["icon"])
            except (KeyError, TypeError): self.icon.append(None)
            try: self.frameUrl.append(x["refObject"]["frameUrl"])
            except (KeyError, TypeError): self.frameUrl.append(None)
            try: self.value.append(x["refObject"]["restrictionInfo"]["restrictValue"])
            except (KeyError, TypeError): self.value.append(None)
        return self

class ChatBubble:
    def __init__(self, data):
        self.json = data

        self.name = []
        self.bubbleId = []
        self.bannerImage = []
        self.backgroundImage = []
        self.resourceUrl = []
        self.value = []

    @property
    def ChatBubble(self):
        for x in self.json:
            try: self.name.append(x["itemBasicInfo"]["name"])
            except (KeyError, TypeError): self.name.append(None)
            try: self.bubbleId.append(x["refObject"]["bubbleId"])
            except (KeyError, TypeError): self.bubbleId.append(None)
            try: self.bannerImage.append(x["refObject"]["bannerImage"])
            except (KeyError, TypeError): self.bannerImage.append(None)
            try: self.backgroundImage.append(x["refObject"]["backgroundImage"])
            except (KeyError, TypeError): self.backgroundImage.append(None)
            try: self.resourceUrl.append(x["refObject"]["resourceUrl"])
            except (KeyError, TypeError): self.resourceUrl.append(None)
            try: self.value.append(x["refObject"]["restrictionInfo"]["restrictValue"])
            except (KeyError, TypeError): self.value.append(None)
        return self

class StoreStickers:
    def __init__(self, data):
        self.json = data

        self.id = []
        self.name = []
        self.icon = []
        self.value = []
        self.smallIcon = []

    @property
    def StoreStickers(self):
        for x in self.json:
            try: self.id.append(x["refObject"]["collectionId"])
            except (KeyError, TypeError): self.id.append(None)
            try: self.name.append(x["itemBasicInfo"]["name"])
            except (KeyError, TypeError): self.name.append(None)
            try: self.icon.append(x["itemBasicInfo"]["icon"])
            except (KeyError, TypeError): self.icon.append(None)
            try: self.value.append(x["refObject"]["restrictionInfo"]["restrictValue"])
            except (KeyError, TypeError): self.value.append(None)
            try: self.smallIcon.append(x["refObject"]["smallIcon"])
            except (KeyError, TypeError): self.smallIcon.append(None)

        return self

class NoticeList:
    def __init__(self, data):
        self.json = data

        self.notificationId = []
        self.noticeId = []
        self.ndcId = []
        self.title = []

        self.targetNickname = []
        self.targetLevel = []
        self.targetReputation = []
        self.targetUid = []

        self.operatorNickname = []
        self.operatorLevel = []
        self.operatorReputation = []
        self.operatorUid = []
        self.operatorRole = []

    @property
    def NoticeList(self):
        for x in self.json:
            try: self.notificationId.append(x["notificationId"])
            except (KeyError, TypeError): self.notificationId.append(None)
            try: self.noticeId.append(x["noticeId"])
            except (KeyError, TypeError): self.noticeId.append(None)
            try: self.ndcId.append(x["ndcId"])
            except (KeyError, TypeError): self.ndcId.append(None)
            try: self.title.append(x["title"])
            except (KeyError, TypeError): self.title.append(None)

            try: self.targetNickname.append(x["targetUser"]["nickname"])
            except (KeyError, TypeError): self.targetNickname.append(None)
            try: self.targetLevel.append(x["targetUser"]["level"])
            except (KeyError, TypeError): self.targetLevel.append(None)
            try: self.targetReputation.append(x["targetUser"]["reputation"])
            except (KeyError, TypeError): self.targetReputation.append(None)
            try: self.targetUid.append(x["targetUser"]["uid"])
            except (KeyError, TypeError): self.targetUid.append(None)

            try: self.operatorNickname.append(x["operator"]["nickname"])
            except (KeyError, TypeError): self.operatorNickname.append(None)
            try: self.operatorLevel.append(x["operator"]["level"])
            except (KeyError, TypeError): self.operatorLevel.append(None)
            try: self.operatorReputation.append(x["operator"]["reputation"])
            except (KeyError, TypeError): self.operatorReputation.append(None)
            try: self.operatorUid.append(x["operator"]["uid"])
            except (KeyError, TypeError): self.operatorUid.append(None)
            try: self.operatorRole.append(x["operator"]["role"])
            except (KeyError, TypeError): self.operatorRole.append(None)


        return self