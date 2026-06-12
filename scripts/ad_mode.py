class AdMode:
    CREATIVE_FILM = "creative_film"
    ECOMMERCE = "ecommerce"
    UGC = "ugc"
    CINEMATIC = "cinematic"
    MULTI_SHOT = "multi_shot"
    ONE_SHOT = "one_shot"
    VIRAL_REPLICATE = "viral_replicate"
    AGENT_MODE = "agent_mode"
    SHORT_DRAMA = "short_drama"

    LABELS = {
        CREATIVE_FILM: "电影创意探索",
        ECOMMERCE: "电商产品",
        UGC: "UGC 原生广告",
        CINEMATIC: "电影感品牌短片",
        MULTI_SHOT: "多镜头叙事",
        ONE_SHOT: "一镜到底",
        VIRAL_REPLICATE: "爆款复刻",
        AGENT_MODE: "Agent 模式（从一句话到成片）",
        SHORT_DRAMA: "短剧创作",
    }

    DEFAULT_SEEDANCE_MODE = {
        CREATIVE_FILM: "text-to-video",
        ECOMMERCE: "image-to-video",
        UGC: "reference-to-video",
        CINEMATIC: "text-to-video",
        MULTI_SHOT: "reference-to-video",
        ONE_SHOT: "image-to-video",
        VIRAL_REPLICATE: "reference-to-video",
        AGENT_MODE: "text-to-video",
        SHORT_DRAMA: "reference-to-video",
    }

    PRODUCT_DOMINANCE_THRESHOLD = 0.4
