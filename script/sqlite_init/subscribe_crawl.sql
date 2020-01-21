/*
 Navicat Premium Data Transfer

 Source Server         : subscribe
 Source Server Type    : SQLite
 Source Server Version : 3021000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3021000
 File Encoding         : 65001

 Date: 21/01/2020 18:30:28
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for subscribe_crawl
-- ----------------------------
DROP TABLE IF EXISTS "subscribe_crawl";
CREATE TABLE "subscribe_crawl" (
  "id" INTEGER NOT NULL,
  "created_at" INTEGER NOT NULL,
  "updated_at" INTEGER NOT NULL,
  "crawl_url" VARCHAR(1000) NOT NULL,
  "crawl_type" INTEGER NOT NULL,
  "rule" JSON NOT NULL,
  "is_closed" INTEGER NOT NULL,
  "next_at" INTEGER NOT NULL,
  "interval" INTEGER NOT NULL,
  "note" TEXT NOT NULL,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of subscribe_crawl
-- ----------------------------
INSERT INTO "subscribe_crawl" VALUES (1, 1571752634, 1579593447, 'https://jiang.netlify.com/', 1, '{"need_proxy": true}', 0, 1579598809, 3600, '');
INSERT INTO "subscribe_crawl" VALUES (2, 1571752634, 1579594634, 'http://youlianboshi.netlify.com/', 1, '{"need_proxy": true}', 0, 1579599163, 3600, '');
INSERT INTO "subscribe_crawl" VALUES (3, 1571752634, 1571752634, 'http://xxx.freev2ray.org/', 2, '{}', 0, 0, 3600, '');
INSERT INTO "subscribe_crawl" VALUES (4, 1571752634, 1579597475, 'http://raw.githubusercontent.com/eycorsican/rule-sets/master/kitsunebi_sub', 1, '{}', 0, 1579601073, 3600, '');
INSERT INTO "subscribe_crawl" VALUES (5, 1571752634, 1579593447, 'http://muma16fx.netlify.com/', 1, '{}', 0, 1579599101, 3600, '');
INSERT INTO "subscribe_crawl" VALUES (7, 1571752634, 1571752634, 'http://v2ray.qlolp.ml/', 0, '{}', 0, 0, 3600, '');
INSERT INTO "subscribe_crawl" VALUES (12, 1571752634, 1579594634, 'https://raw.githubusercontent.com/voken100g/AutoSSR/master/recent', 1, '{}', 0, 1579598656, 3600, '');
INSERT INTO "subscribe_crawl" VALUES (13, 1571752634, 1579594634, 'https://git.io/autossr_recent', 1, '{}', 0, 1579598834, 3600, '');
INSERT INTO "subscribe_crawl" VALUES (14, 1571752634, 1579594634, 'https://git.io/autossr_stable', 1, '{}', 0, 1579599154, 3600, '');
INSERT INTO "subscribe_crawl" VALUES (15, 1571752634, 1579594634, 'https://raw.githubusercontent.com/voken100g/AutoSSR/master/stable', 1, '{}', 0, 1579599819, 3600, '');
INSERT INTO "subscribe_crawl" VALUES (16, 1571752634, 1579594634, 'https://raw.githubusercontent.com/ssrsub/ssr/master/ssrsub', 1, '{"need_proxy": true}', 0, 1579599262, 3600, '');
INSERT INTO "subscribe_crawl" VALUES (17, 1571752634, 1579594634, 'https://muma16fx.netlify.com', 1, '{}', 0, 1579599497, 3600, '');
INSERT INTO "subscribe_crawl" VALUES (19, 1571752634, 1579597475, 'http://jiang.netlify.com', 1, '{}', 0, 1579600172, 3600, '');
INSERT INTO "subscribe_crawl" VALUES (22, 1571752634, 1579597475, 'https://www.liesauer.net/yogurt/subscribe?ACCESS_TOKEN=DAYxR3mMaZAsaqUb', 1, '{}', 0, 1579599315, 3600, '');
INSERT INTO "subscribe_crawl" VALUES (23, 1571752634, 1579594634, 'https://yzzz.ml/freessr/', 1, '{}', 0, 1579599766, 3600, '');
INSERT INTO "subscribe_crawl" VALUES (24, 1571752634, 1579594634, 'https://raw.githubusercontent.com/voken100g/AutoSSR/master/online', 1, '{}', 0, 1579599476, 3600, '');
INSERT INTO "subscribe_crawl" VALUES (25, 1571752634, 1579597475, 'http://qiaomenzhuanfx.netlify.com/', 1, '{"need_proxy": true}', 0, 1579602987, 3600, '');

PRAGMA foreign_keys = true;
