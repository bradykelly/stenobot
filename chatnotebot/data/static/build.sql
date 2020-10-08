-- From Solaris: https://github.com/parafoxia/Solaris

CREATE TABLE IF NOT EXISTS bot (
    Key text PRIMARY KEY,
    Value text
);

INSERT OR IGNORE INTO bot VALUES ("last commit", CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS errors (
    Ref text PRIMARY KEY,
    ErrorTime text DEFAULT CURRENT_TIMESTAMP,
    Cause text,
    Traceback text
);

CREATE TABLE IF NOT EXISTS guild_config (
    GuildID integer PRIMARY KEY,
    RunFTS integer DEFAULT 0,
    Prefix text DEFAULT ">>",
    DefaultLogChannelID integer,
    LogChannelID integer,
    DefaultAdminRoleID interger,
    AdminRoleID integer
);

-- gateway

CREATE TABLE IF NOT EXISTS gateway (
	GuildID integer PRIMARY KEY,
	Active integer DEFAULT 0,
	RulesChannelID integer,
	GateMessageID integer,
	BlockingRoleID integer,
	MemberRoleIDs text,
	ExceptionRoleIDs text,
	WelcomeChannelID integer,
	GoodbyeChannelID integer,
	Timeout integer,
	GateText text,
	WelcomeText text,
	WelcomeBotText text,
	GoodbyeText text,
	GoodbyeBotText text
);

CREATE TABLE IF NOT EXISTS entrants (
	GuildID integer,
	UserID integer,
	Timeout text,
	PRIMARY KEY (GuildID, UserID)
);

CREATE TABLE IF NOT EXISTS accepted (
	GuildID integer,
	UserID integer,
	PRIMARY KEY (GuildID, UserID)
);

-- warn

CREATE TABLE IF NOT EXISTS warn (
	GuildID integer PRIMARY KEY,
	WarnRoleID integer,
	MaxPoints integer,
	MaxStrikes interger
);

CREATE TABLE IF NOT EXISTS warntypes (
	GuildID integer,
	WarnType text,
	Points integer,
	PRIMARY KEY (GuildID, WarnType)
);

CREATE TABLE IF NOT EXISTS warns (
	WarnID text PRIMARY KEY,
	GuildID integer,
	UserID integer,
	ModID integer,
	WarnTime text DEFAULT CURRENT_TIMESTAMP,
	WarnType text,
	Comment text
);
