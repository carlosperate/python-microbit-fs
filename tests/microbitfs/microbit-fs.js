"use strict";
var microbitFs = (() => {
  var __create = Object.create;
  var __defProp = Object.defineProperty;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __getProtoOf = Object.getPrototypeOf;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __commonJS = (cb, mod) => function __require() {
    return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
  };
  var __export = (target, all) => {
    for (var name in all)
      __defProp(target, name, { get: all[name], enumerable: true });
  };
  var __copyProps = (to, from, except, desc) => {
    if (from && typeof from === "object" || typeof from === "function") {
      for (let key of __getOwnPropNames(from))
        if (!__hasOwnProp.call(to, key) && key !== except)
          __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
    }
    return to;
  };
  var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
    // If the importer is in node compatibility mode or this is not an ESM
    // file that has been converted to a CommonJS file using a Babel-
    // compatible transform (i.e. "__esModule" has not been set), then set
    // "default" to the CommonJS "module.exports" for node compatibility.
    isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
    mod
  ));
  var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

  // node_modules/nrf-intel-hex/intel-hex.browser.js
  var require_intel_hex_browser = __commonJS({
    "node_modules/nrf-intel-hex/intel-hex.browser.js"(exports, module) {
      (function(global, factory) {
        typeof exports === "object" && typeof module !== "undefined" ? module.exports = factory() : typeof define === "function" && define.amd ? define(factory) : global.MemoryMap = factory();
      })(exports, function() {
        "use strict";
        var hexLineRegexp = /:([0-9A-Fa-f]{8,})([0-9A-Fa-f]{2})(?:\r\n|\r|\n|)/g;
        function checksum(bytes) {
          return -bytes.reduce(function(sum, v) {
            return sum + v;
          }, 0) & 255;
        }
        function checksumTwo(array1, array2) {
          var partial1 = array1.reduce(function(sum, v) {
            return sum + v;
          }, 0);
          var partial2 = array2.reduce(function(sum, v) {
            return sum + v;
          }, 0);
          return -(partial1 + partial2) & 255;
        }
        function hexpad(number) {
          return number.toString(16).toUpperCase().padStart(2, "0");
        }
        Number.isInteger = Number.isInteger || function(value) {
          return typeof value === "number" && isFinite(value) && Math.floor(value) === value;
        };
        var MemoryMap6 = function MemoryMap7(blocks) {
          var this$1 = this;
          this._blocks = /* @__PURE__ */ new Map();
          if (blocks && typeof blocks[Symbol.iterator] === "function") {
            for (var tuple of blocks) {
              if (!(tuple instanceof Array) || tuple.length !== 2) {
                throw new Error("First parameter to MemoryMap constructor must be an iterable of [addr, bytes] or undefined");
              }
              this$1.set(tuple[0], tuple[1]);
            }
          } else if (typeof blocks === "object") {
            var addrs = Object.keys(blocks);
            for (var addr of addrs) {
              this$1.set(parseInt(addr), blocks[addr]);
            }
          } else if (blocks !== void 0 && blocks !== null) {
            throw new Error("First parameter to MemoryMap constructor must be an iterable of [addr, bytes] or undefined");
          }
        };
        var prototypeAccessors = { size: { configurable: true } };
        MemoryMap6.prototype.set = function set(addr, value) {
          if (!Number.isInteger(addr)) {
            throw new Error("Address passed to MemoryMap is not an integer");
          }
          if (addr < 0) {
            throw new Error("Address passed to MemoryMap is negative");
          }
          if (!(value instanceof Uint8Array)) {
            throw new Error("Bytes passed to MemoryMap are not an Uint8Array");
          }
          return this._blocks.set(addr, value);
        };
        MemoryMap6.prototype.get = function get(addr) {
          return this._blocks.get(addr);
        };
        MemoryMap6.prototype.clear = function clear() {
          return this._blocks.clear();
        };
        MemoryMap6.prototype.delete = function delete$1(addr) {
          return this._blocks.delete(addr);
        };
        MemoryMap6.prototype.entries = function entries() {
          return this._blocks.entries();
        };
        MemoryMap6.prototype.forEach = function forEach(callback, that) {
          return this._blocks.forEach(callback, that);
        };
        MemoryMap6.prototype.has = function has(addr) {
          return this._blocks.has(addr);
        };
        MemoryMap6.prototype.keys = function keys() {
          return this._blocks.keys();
        };
        MemoryMap6.prototype.values = function values() {
          return this._blocks.values();
        };
        prototypeAccessors.size.get = function() {
          return this._blocks.size;
        };
        MemoryMap6.prototype[Symbol.iterator] = function() {
          return this._blocks[Symbol.iterator]();
        };
        MemoryMap6.fromHex = function fromHex(hexText, maxBlockSize) {
          if (maxBlockSize === void 0) maxBlockSize = Infinity;
          var blocks = new MemoryMap6();
          var lastCharacterParsed = 0;
          var matchResult;
          var recordCount = 0;
          var ulba = 0;
          hexLineRegexp.lastIndex = 0;
          while ((matchResult = hexLineRegexp.exec(hexText)) !== null) {
            recordCount++;
            if (lastCharacterParsed !== matchResult.index) {
              throw new Error(
                "Malformed hex file: Could not parse between characters " + lastCharacterParsed + " and " + matchResult.index + ' ("' + hexText.substring(lastCharacterParsed, Math.min(matchResult.index, lastCharacterParsed + 16)).trim() + '")'
              );
            }
            lastCharacterParsed = hexLineRegexp.lastIndex;
            var recordStr = matchResult[1];
            var recordChecksum = matchResult[2];
            var recordBytes = new Uint8Array(recordStr.match(/[\da-f]{2}/gi).map(function(h) {
              return parseInt(h, 16);
            }));
            var recordLength = recordBytes[0];
            if (recordLength + 4 !== recordBytes.length) {
              throw new Error("Mismatched record length at record " + recordCount + " (" + matchResult[0].trim() + "), expected " + recordLength + " data bytes but actual length is " + (recordBytes.length - 4));
            }
            var cs = checksum(recordBytes);
            if (parseInt(recordChecksum, 16) !== cs) {
              throw new Error("Checksum failed at record " + recordCount + " (" + matchResult[0].trim() + "), should be " + cs.toString(16));
            }
            var offset = (recordBytes[1] << 8) + recordBytes[2];
            var recordType = recordBytes[3];
            var data = recordBytes.subarray(4);
            if (recordType === 0) {
              if (blocks.has(ulba + offset)) {
                throw new Error("Duplicated data at record " + recordCount + " (" + matchResult[0].trim() + ")");
              }
              if (offset + data.length > 65536) {
                throw new Error(
                  "Data at record " + recordCount + " (" + matchResult[0].trim() + ") wraps over 0xFFFF. This would trigger ambiguous behaviour. Please restructure your data so that for every record the data offset plus the data length do not exceed 0xFFFF."
                );
              }
              blocks.set(ulba + offset, data);
            } else {
              if (offset !== 0) {
                throw new Error("Record " + recordCount + " (" + matchResult[0].trim() + ") must have 0000 as data offset.");
              }
              switch (recordType) {
                case 1:
                  if (lastCharacterParsed !== hexText.length) {
                    throw new Error("There is data after an EOF record at record " + recordCount);
                  }
                  return blocks.join(maxBlockSize);
                case 2:
                  ulba = (data[0] << 8) + data[1] << 4;
                  break;
                case 3:
                  break;
                case 4:
                  ulba = (data[0] << 8) + data[1] << 16;
                  break;
                case 5:
                  break;
                default:
                  throw new Error("Invalid record type 0x" + hexpad(recordType) + " at record " + recordCount + " (should be between 0x00 and 0x05)");
              }
            }
          }
          if (recordCount) {
            throw new Error("No EOF record at end of file");
          } else {
            throw new Error("Malformed .hex file, could not parse any registers");
          }
        };
        MemoryMap6.prototype.join = function join(maxBlockSize) {
          var this$1 = this;
          if (maxBlockSize === void 0) maxBlockSize = Infinity;
          var sortedKeys = Array.from(this.keys()).sort(function(a, b) {
            return a - b;
          });
          var blockSizes = /* @__PURE__ */ new Map();
          var lastBlockAddr = -1;
          var lastBlockEndAddr = -1;
          for (var i = 0, l = sortedKeys.length; i < l; i++) {
            var blockAddr = sortedKeys[i];
            var blockLength = this$1.get(sortedKeys[i]).length;
            if (lastBlockEndAddr === blockAddr && lastBlockEndAddr - lastBlockAddr < maxBlockSize) {
              blockSizes.set(lastBlockAddr, blockSizes.get(lastBlockAddr) + blockLength);
              lastBlockEndAddr += blockLength;
            } else if (lastBlockEndAddr <= blockAddr) {
              blockSizes.set(blockAddr, blockLength);
              lastBlockAddr = blockAddr;
              lastBlockEndAddr = blockAddr + blockLength;
            } else {
              throw new Error("Overlapping data around address 0x" + blockAddr.toString(16));
            }
          }
          var mergedBlocks = new MemoryMap6();
          var mergingBlock;
          var mergingBlockAddr = -1;
          for (var i$1 = 0, l$1 = sortedKeys.length; i$1 < l$1; i$1++) {
            var blockAddr$1 = sortedKeys[i$1];
            if (blockSizes.has(blockAddr$1)) {
              mergingBlock = new Uint8Array(blockSizes.get(blockAddr$1));
              mergedBlocks.set(blockAddr$1, mergingBlock);
              mergingBlockAddr = blockAddr$1;
            }
            mergingBlock.set(this$1.get(blockAddr$1), blockAddr$1 - mergingBlockAddr);
          }
          return mergedBlocks;
        };
        MemoryMap6.overlapMemoryMaps = function overlapMemoryMaps(memoryMaps) {
          var cuts = /* @__PURE__ */ new Set();
          for (var [, blocks] of memoryMaps) {
            for (var [address, block] of blocks) {
              cuts.add(address);
              cuts.add(address + block.length);
            }
          }
          var orderedCuts = Array.from(cuts.values()).sort(function(a, b) {
            return a - b;
          });
          var overlaps = /* @__PURE__ */ new Map();
          var loop = function(i2, l2) {
            var cut = orderedCuts[i2];
            var nextCut = orderedCuts[i2 + 1];
            var tuples = [];
            for (var [setId, blocks$1] of memoryMaps) {
              var blockAddr = Array.from(blocks$1.keys()).reduce(function(acc, val) {
                if (val > cut) {
                  return acc;
                }
                return Math.max(acc, val);
              }, -1);
              if (blockAddr !== -1) {
                var block$1 = blocks$1.get(blockAddr);
                var subBlockStart = cut - blockAddr;
                var subBlockEnd = nextCut - blockAddr;
                if (subBlockStart < block$1.length) {
                  tuples.push([setId, block$1.subarray(subBlockStart, subBlockEnd)]);
                }
              }
            }
            if (tuples.length) {
              overlaps.set(cut, tuples);
            }
          };
          for (var i = 0, l = orderedCuts.length - 1; i < l; i++) loop(i, l);
          return overlaps;
        };
        MemoryMap6.flattenOverlaps = function flattenOverlaps(overlaps) {
          return new MemoryMap6(
            Array.from(overlaps.entries()).map(function(ref) {
              var address = ref[0];
              var tuples = ref[1];
              return [address, tuples[tuples.length - 1][1]];
            })
          );
        };
        MemoryMap6.prototype.paginate = function paginate(pageSize, pad) {
          var this$1 = this;
          if (pageSize === void 0) pageSize = 1024;
          if (pad === void 0) pad = 255;
          if (pageSize <= 0) {
            throw new Error("Page size must be greater than zero");
          }
          var outPages = new MemoryMap6();
          var page;
          var sortedKeys = Array.from(this.keys()).sort(function(a, b) {
            return a - b;
          });
          for (var i = 0, l = sortedKeys.length; i < l; i++) {
            var blockAddr = sortedKeys[i];
            var block = this$1.get(blockAddr);
            var blockLength = block.length;
            var blockEnd = blockAddr + blockLength;
            for (var pageAddr = blockAddr - blockAddr % pageSize; pageAddr < blockEnd; pageAddr += pageSize) {
              page = outPages.get(pageAddr);
              if (!page) {
                page = new Uint8Array(pageSize);
                page.fill(pad);
                outPages.set(pageAddr, page);
              }
              var offset = pageAddr - blockAddr;
              var subBlock = void 0;
              if (offset <= 0) {
                subBlock = block.subarray(0, Math.min(pageSize + offset, blockLength));
                page.set(subBlock, -offset);
              } else {
                subBlock = block.subarray(offset, offset + Math.min(pageSize, blockLength - offset));
                page.set(subBlock, 0);
              }
            }
          }
          return outPages;
        };
        MemoryMap6.prototype.getUint32 = function getUint322(offset, littleEndian) {
          var this$1 = this;
          var keys = Array.from(this.keys());
          for (var i = 0, l = keys.length; i < l; i++) {
            var blockAddr = keys[i];
            var block = this$1.get(blockAddr);
            var blockLength = block.length;
            var blockEnd = blockAddr + blockLength;
            if (blockAddr <= offset && offset + 4 <= blockEnd) {
              return new DataView(block.buffer, offset - blockAddr, 4).getUint32(0, littleEndian);
            }
          }
          return;
        };
        MemoryMap6.prototype.asHexString = function asHexString(lineSize) {
          var this$1 = this;
          if (lineSize === void 0) lineSize = 16;
          var lowAddress = 0;
          var highAddress = -1 << 16;
          var records = [];
          if (lineSize <= 0) {
            throw new Error("Size of record must be greater than zero");
          } else if (lineSize > 255) {
            throw new Error("Size of record must be less than 256");
          }
          var offsetRecord = new Uint8Array(6);
          var recordHeader = new Uint8Array(4);
          var sortedKeys = Array.from(this.keys()).sort(function(a, b) {
            return a - b;
          });
          for (var i = 0, l = sortedKeys.length; i < l; i++) {
            var blockAddr = sortedKeys[i];
            var block = this$1.get(blockAddr);
            if (!(block instanceof Uint8Array)) {
              throw new Error("Block at offset " + blockAddr + " is not an Uint8Array");
            }
            if (blockAddr < 0) {
              throw new Error("Block at offset " + blockAddr + " has a negative thus invalid address");
            }
            var blockSize = block.length;
            if (!blockSize) {
              continue;
            }
            if (blockAddr > highAddress + 65535) {
              highAddress = blockAddr - blockAddr % 65536;
              lowAddress = 0;
              offsetRecord[0] = 2;
              offsetRecord[1] = 0;
              offsetRecord[2] = 0;
              offsetRecord[3] = 4;
              offsetRecord[4] = highAddress >> 24;
              offsetRecord[5] = highAddress >> 16;
              records.push(
                ":" + Array.prototype.map.call(offsetRecord, hexpad).join("") + hexpad(checksum(offsetRecord))
              );
            }
            if (blockAddr < highAddress + lowAddress) {
              throw new Error(
                "Block starting at 0x" + blockAddr.toString(16) + " overlaps with a previous block."
              );
            }
            lowAddress = blockAddr % 65536;
            var blockOffset = 0;
            var blockEnd = blockAddr + blockSize;
            if (blockEnd > 4294967295) {
              throw new Error("Data cannot be over 0xFFFFFFFF");
            }
            while (highAddress + lowAddress < blockEnd) {
              if (lowAddress > 65535) {
                highAddress += 1 << 16;
                lowAddress = 0;
                offsetRecord[0] = 2;
                offsetRecord[1] = 0;
                offsetRecord[2] = 0;
                offsetRecord[3] = 4;
                offsetRecord[4] = highAddress >> 24;
                offsetRecord[5] = highAddress >> 16;
                records.push(
                  ":" + Array.prototype.map.call(offsetRecord, hexpad).join("") + hexpad(checksum(offsetRecord))
                );
              }
              var recordSize = -1;
              while (lowAddress < 65536 && recordSize) {
                recordSize = Math.min(
                  lineSize,
                  // Normal case
                  blockEnd - highAddress - lowAddress,
                  // End of block
                  65536 - lowAddress
                  // End of low addresses
                );
                if (recordSize) {
                  recordHeader[0] = recordSize;
                  recordHeader[1] = lowAddress >> 8;
                  recordHeader[2] = lowAddress;
                  recordHeader[3] = 0;
                  var subBlock = block.subarray(blockOffset, blockOffset + recordSize);
                  records.push(
                    ":" + Array.prototype.map.call(recordHeader, hexpad).join("") + Array.prototype.map.call(subBlock, hexpad).join("") + hexpad(checksumTwo(recordHeader, subBlock))
                  );
                  blockOffset += recordSize;
                  lowAddress += recordSize;
                }
              }
            }
          }
          records.push(":00000001FF");
          return records.join("\n");
        };
        MemoryMap6.prototype.clone = function clone() {
          var this$1 = this;
          var cloned = new MemoryMap6();
          for (var [addr, value] of this$1) {
            cloned.set(addr, new Uint8Array(value));
          }
          return cloned;
        };
        MemoryMap6.fromPaddedUint8Array = function fromPaddedUint8Array(bytes, padByte, minPadLength) {
          if (padByte === void 0) padByte = 255;
          if (minPadLength === void 0) minPadLength = 64;
          if (!(bytes instanceof Uint8Array)) {
            throw new Error("Bytes passed to fromPaddedUint8Array are not an Uint8Array");
          }
          var memMap = new MemoryMap6();
          var consecutivePads = 0;
          var lastNonPad = -1;
          var firstNonPad = 0;
          var skippingBytes = false;
          var l = bytes.length;
          for (var addr = 0; addr < l; addr++) {
            var byte = bytes[addr];
            if (byte === padByte) {
              consecutivePads++;
              if (consecutivePads >= minPadLength) {
                if (lastNonPad !== -1) {
                  memMap.set(firstNonPad, bytes.subarray(firstNonPad, lastNonPad + 1));
                }
                skippingBytes = true;
              }
            } else {
              if (skippingBytes) {
                skippingBytes = false;
                firstNonPad = addr;
              }
              lastNonPad = addr;
              consecutivePads = 0;
            }
          }
          if (!skippingBytes && lastNonPad !== -1) {
            memMap.set(firstNonPad, bytes.subarray(firstNonPad, l));
          }
          return memMap;
        };
        MemoryMap6.prototype.slice = function slice(address, length) {
          var this$1 = this;
          if (length === void 0) length = Infinity;
          if (length < 0) {
            throw new Error("Length of the slice cannot be negative");
          }
          var sliced = new MemoryMap6();
          for (var [blockAddr, block] of this$1) {
            var blockLength = block.length;
            if (blockAddr + blockLength >= address && blockAddr < address + length) {
              var sliceStart = Math.max(address, blockAddr);
              var sliceEnd = Math.min(address + length, blockAddr + blockLength);
              var sliceLength = sliceEnd - sliceStart;
              var relativeSliceStart = sliceStart - blockAddr;
              if (sliceLength > 0) {
                sliced.set(sliceStart, block.subarray(relativeSliceStart, relativeSliceStart + sliceLength));
              }
            }
          }
          return sliced;
        };
        MemoryMap6.prototype.slicePad = function slicePad(address, length, padByte) {
          var this$1 = this;
          if (padByte === void 0) padByte = 255;
          if (length < 0) {
            throw new Error("Length of the slice cannot be negative");
          }
          var out = new Uint8Array(length).fill(padByte);
          for (var [blockAddr, block] of this$1) {
            var blockLength = block.length;
            if (blockAddr + blockLength >= address && blockAddr < address + length) {
              var sliceStart = Math.max(address, blockAddr);
              var sliceEnd = Math.min(address + length, blockAddr + blockLength);
              var sliceLength = sliceEnd - sliceStart;
              var relativeSliceStart = sliceStart - blockAddr;
              if (sliceLength > 0) {
                out.set(block.subarray(relativeSliceStart, relativeSliceStart + sliceLength), sliceStart - address);
              }
            }
          }
          return out;
        };
        MemoryMap6.prototype.contains = function contains(memMap) {
          var this$1 = this;
          for (var [blockAddr, block] of memMap) {
            var blockLength = block.length;
            var slice = this$1.slice(blockAddr, blockLength).join().get(blockAddr);
            if (!slice || slice.length !== blockLength) {
              return false;
            }
            for (var i in block) {
              if (block[i] !== slice[i]) {
                return false;
              }
            }
          }
          return true;
        };
        Object.defineProperties(MemoryMap6.prototype, prototypeAccessors);
        return MemoryMap6;
      });
    }
  });

  // src/index.ts
  var index_exports = {};
  __export(index_exports, {
    AppendedBlock: () => AppendedBlock,
    MicropythonFsHex: () => MicropythonFsHex,
    addIntelHexAppendedScript: () => addIntelHexAppendedScript,
    cleanseOldHexFormat: () => cleanseOldHexFormat,
    getHexMapDeviceMemInfo: () => getHexMapDeviceMemInfo,
    getIntelHexAppendedScript: () => getIntelHexAppendedScript,
    getIntelHexDeviceMemInfo: () => getIntelHexDeviceMemInfo,
    isAppendedScriptPresent: () => isAppendedScriptPresent,
    microbitBoardId: () => microbitBoardId2
  });

  // src/micropython-appended.ts
  var import_nrf_intel_hex = __toESM(require_intel_hex_browser());

  // src/common.ts
  function strToBytes(str) {
    const encoder = new TextEncoder();
    return encoder.encode(str);
  }
  function bytesToStr(byteArray) {
    const decoder = new TextDecoder();
    return decoder.decode(byteArray);
  }
  var concatUint8Array = (first, second) => {
    const combined = new Uint8Array(first.length + second.length);
    combined.set(first);
    combined.set(second, first.length);
    return combined;
  };
  var areUint8ArraysEqual = (first, second) => {
    if (first.length !== second.length) return false;
    for (let i = 0; i < first.length; i++) {
      if (first[i] !== second[i]) return false;
    }
    return true;
  };

  // src/micropython-appended.ts
  var AppendedBlock = /* @__PURE__ */ ((AppendedBlock2) => {
    AppendedBlock2[AppendedBlock2["StartAdd"] = 253952] = "StartAdd";
    AppendedBlock2[AppendedBlock2["Length"] = 8192] = "Length";
    AppendedBlock2[AppendedBlock2["EndAdd"] = 262144] = "EndAdd";
    return AppendedBlock2;
  })(AppendedBlock || {});
  var HEADER_START_BYTE_0 = 77;
  var HEADER_START_BYTE_1 = 80;
  var HEX_RECORD_DATA_LEN = 16;
  var HEX_INSERTION_POINT = ":::::::::::::::::::::::::::::::::::::::::::\n";
  function cleanseOldHexFormat(intelHex) {
    return intelHex.replace(HEX_INSERTION_POINT, "");
  }
  function getIntelHexAppendedScript(intelHex) {
    let pyCode = "";
    const hexFileMemMap = import_nrf_intel_hex.default.fromHex(intelHex);
    if (hexFileMemMap.has(253952 /* StartAdd */)) {
      const pyCodeMemMap = hexFileMemMap.slice(
        253952 /* StartAdd */,
        8192 /* Length */
      );
      const codeBytes = pyCodeMemMap.get(253952 /* StartAdd */);
      if (codeBytes[0 /* Byte0 */] === HEADER_START_BYTE_0 && codeBytes[1 /* Byte1 */] === HEADER_START_BYTE_1) {
        pyCode = bytesToStr(codeBytes.slice(4 /* Length */));
        pyCode = pyCode.replace(/\0/g, "");
      }
    }
    return pyCode;
  }
  function createAppendedBlock(dataBytes) {
    let blockLength = dataBytes.length + 4 /* Length */;
    if (blockLength % HEX_RECORD_DATA_LEN) {
      blockLength += HEX_RECORD_DATA_LEN - blockLength % HEX_RECORD_DATA_LEN;
    }
    const blockBytes = new Uint8Array(blockLength).fill(0);
    blockBytes[0] = HEADER_START_BYTE_0;
    blockBytes[1] = HEADER_START_BYTE_1;
    blockBytes[2] = dataBytes.length & 255;
    blockBytes[3] = dataBytes.length >> 8 & 255;
    blockBytes.set(dataBytes, 4 /* Length */);
    return blockBytes;
  }
  function addIntelHexAppendedScript(intelHex, pyCode) {
    const codeBytes = strToBytes(pyCode);
    const blockBytes = createAppendedBlock(codeBytes);
    if (blockBytes.length > 8192 /* Length */) {
      throw new RangeError("Too long");
    }
    const intelHexClean = cleanseOldHexFormat(intelHex);
    const intelHexMap = import_nrf_intel_hex.default.fromHex(intelHexClean);
    intelHexMap.set(253952 /* StartAdd */, blockBytes);
    return intelHexMap.asHexString() + "\n";
  }
  function isAppendedScriptPresent(intelHex) {
    let intelHexMap;
    if (typeof intelHex === "string") {
      const intelHexClean = cleanseOldHexFormat(intelHex);
      intelHexMap = import_nrf_intel_hex.default.fromHex(intelHexClean);
    } else {
      intelHexMap = intelHex;
    }
    const headerMagic = intelHexMap.slicePad(253952 /* StartAdd */, 2, 255);
    return headerMagic[0] === HEADER_START_BYTE_0 && headerMagic[1] === HEADER_START_BYTE_1;
  }

  // node_modules/@microbit/microbit-universal-hex/dist/esm5/utils.js
  function hexStrToBytes(hexStr) {
    if (hexStr.length % 2 !== 0) {
      throw new Error('Hex string "' + hexStr + '" is not divisible by 2.');
    }
    var byteArray = hexStr.match(/.{1,2}/g);
    if (byteArray) {
      return new Uint8Array(byteArray.map(function(byteStr) {
        var byteNum = parseInt(byteStr, 16);
        if (Number.isNaN(byteNum)) {
          throw new Error('There were some non-hex characters in "' + hexStr + '".');
        } else {
          return byteNum;
        }
      }));
    } else {
      return new Uint8Array();
    }
  }
  function byteToHexStrFast(byte) {
    return byte.toString(16).toUpperCase().padStart(2, "0");
  }
  function byteArrayToHexStr(byteArray) {
    return byteArray.reduce(function(accumulator, current) {
      return accumulator + current.toString(16).toUpperCase().padStart(2, "0");
    }, "");
  }
  function concatUint8Arrays(arraysToConcat) {
    var fullLength = arraysToConcat.reduce(function(accumulator, currentValue) {
      return accumulator + currentValue.length;
    }, 0);
    var combined = new Uint8Array(fullLength);
    arraysToConcat.reduce(function(accumulator, currentArray) {
      combined.set(currentArray, accumulator);
      return accumulator + currentArray.length;
    }, 0);
    return combined;
  }

  // node_modules/@microbit/microbit-universal-hex/dist/esm5/ihex.js
  var RecordType;
  (function(RecordType2) {
    RecordType2[RecordType2["Data"] = 0] = "Data";
    RecordType2[RecordType2["EndOfFile"] = 1] = "EndOfFile";
    RecordType2[RecordType2["ExtendedSegmentAddress"] = 2] = "ExtendedSegmentAddress";
    RecordType2[RecordType2["StartSegmentAddress"] = 3] = "StartSegmentAddress";
    RecordType2[RecordType2["ExtendedLinearAddress"] = 4] = "ExtendedLinearAddress";
    RecordType2[RecordType2["StartLinearAddress"] = 5] = "StartLinearAddress";
    RecordType2[RecordType2["BlockStart"] = 10] = "BlockStart";
    RecordType2[RecordType2["BlockEnd"] = 11] = "BlockEnd";
    RecordType2[RecordType2["PaddedData"] = 12] = "PaddedData";
    RecordType2[RecordType2["CustomData"] = 13] = "CustomData";
    RecordType2[RecordType2["OtherData"] = 14] = "OtherData";
  })(RecordType || (RecordType = {}));
  var RECORD_DATA_MAX_BYTES = 32;
  var START_CODE_STR = ":";
  var START_CODE_INDEX = 0;
  var START_CODE_STR_LEN = START_CODE_STR.length;
  var BYTE_COUNT_STR_INDEX = START_CODE_INDEX + START_CODE_STR_LEN;
  var BYTE_COUNT_STR_LEN = 2;
  var ADDRESS_STR_INDEX = BYTE_COUNT_STR_INDEX + BYTE_COUNT_STR_LEN;
  var ADDRESS_STR_LEN = 4;
  var RECORD_TYPE_STR_INDEX = ADDRESS_STR_INDEX + ADDRESS_STR_LEN;
  var RECORD_TYPE_STR_LEN = 2;
  var DATA_STR_INDEX = RECORD_TYPE_STR_INDEX + RECORD_TYPE_STR_LEN;
  var DATA_STR_LEN_MIN = 0;
  var CHECKSUM_STR_LEN = 2;
  var MIN_RECORD_STR_LEN = START_CODE_STR_LEN + BYTE_COUNT_STR_LEN + ADDRESS_STR_LEN + RECORD_TYPE_STR_LEN + DATA_STR_LEN_MIN + CHECKSUM_STR_LEN;
  var MAX_RECORD_STR_LEN = MIN_RECORD_STR_LEN - DATA_STR_LEN_MIN + RECORD_DATA_MAX_BYTES * 2;
  function isRecordTypeValid(recordType) {
    if (recordType >= RecordType.Data && recordType <= RecordType.StartLinearAddress || recordType >= RecordType.BlockStart && recordType <= RecordType.OtherData) {
      return true;
    }
    return false;
  }
  function calcChecksumByte(dataBytes) {
    var sum = dataBytes.reduce(function(accumulator, currentValue) {
      return accumulator + currentValue;
    }, 0);
    return -sum & 255;
  }
  function createRecord(address, recordType, dataBytes) {
    if (address < 0 || address > 65535) {
      throw new Error("Record (" + recordType + ") address out of range: " + address);
    }
    var byteCount = dataBytes.length;
    if (byteCount > RECORD_DATA_MAX_BYTES) {
      throw new Error("Record (" + recordType + ") data has too many bytes (" + byteCount + ").");
    }
    if (!isRecordTypeValid(recordType)) {
      throw new Error("Record type '" + recordType + "' is not valid.");
    }
    var recordContent = concatUint8Arrays([
      new Uint8Array([byteCount, address >> 8, address & 255, recordType]),
      dataBytes
    ]);
    var recordContentStr = byteArrayToHexStr(recordContent);
    var checksumStr = byteToHexStrFast(calcChecksumByte(recordContent));
    return "" + START_CODE_STR + recordContentStr + checksumStr;
  }
  function validateRecord(iHexRecord) {
    if (iHexRecord.length < MIN_RECORD_STR_LEN) {
      throw new Error("Record length too small: " + iHexRecord);
    }
    if (iHexRecord.length > MAX_RECORD_STR_LEN) {
      throw new Error("Record length is too large: " + iHexRecord);
    }
    if (iHexRecord[0] !== ":") {
      throw new Error('Record does not start with a ":": ' + iHexRecord);
    }
    return true;
  }
  function getRecordType(iHexRecord) {
    validateRecord(iHexRecord);
    var recordTypeCharStart = START_CODE_STR_LEN + BYTE_COUNT_STR_LEN + ADDRESS_STR_LEN;
    var recordTypeStr = iHexRecord.slice(recordTypeCharStart, recordTypeCharStart + RECORD_TYPE_STR_LEN);
    var recordType = parseInt(recordTypeStr, 16);
    if (!isRecordTypeValid(recordType)) {
      throw new Error("Record type '" + recordTypeStr + "' from record '" + iHexRecord + "' is not valid.");
    }
    return recordType;
  }
  function getRecordData(iHexRecord) {
    try {
      return hexStrToBytes(iHexRecord.slice(DATA_STR_INDEX, -2));
    } catch (e) {
      throw new Error('Could not parse Intel Hex record "' + iHexRecord + '": ' + e.message);
    }
  }
  function parseRecord(iHexRecord) {
    validateRecord(iHexRecord);
    var recordBytes;
    try {
      recordBytes = hexStrToBytes(iHexRecord.substring(1));
    } catch (e) {
      throw new Error('Could not parse Intel Hex record "' + iHexRecord + '": ' + e.message);
    }
    var byteCountIndex = 0;
    var byteCount = recordBytes[0];
    var addressIndex = byteCountIndex + BYTE_COUNT_STR_LEN / 2;
    var address = (recordBytes[addressIndex] << 8) + recordBytes[addressIndex + 1];
    var recordTypeIndex = addressIndex + ADDRESS_STR_LEN / 2;
    var recordType = recordBytes[recordTypeIndex];
    var dataIndex = recordTypeIndex + RECORD_TYPE_STR_LEN / 2;
    var checksumIndex = dataIndex + byteCount;
    var data = recordBytes.slice(dataIndex, checksumIndex);
    var checksum = recordBytes[checksumIndex];
    var totalLength = checksumIndex + CHECKSUM_STR_LEN / 2;
    if (recordBytes.length > totalLength) {
      throw new Error('Parsed record "' + iHexRecord + '" is larger than indicated by the byte count.' + ("\n	Expected: " + totalLength + "; Length: " + recordBytes.length + "."));
    }
    return {
      byteCount,
      address,
      recordType,
      data,
      checksum
    };
  }
  function endOfFileRecord() {
    return ":00000001FF";
  }
  function extLinAddressRecord(address) {
    if (address < 0 || address > 4294967295) {
      throw new Error("Address '" + address + "' for Extended Linear Address record is out of range.");
    }
    return createRecord(0, RecordType.ExtendedLinearAddress, new Uint8Array([address >> 24 & 255, address >> 16 & 255]));
  }
  function blockStartRecord(boardId) {
    if (boardId < 0 || boardId > 65535) {
      throw new Error("Board ID out of range when creating Block Start record.");
    }
    return createRecord(0, RecordType.BlockStart, new Uint8Array([boardId >> 8 & 255, boardId & 255, 192, 222]));
  }
  function blockEndRecord(padBytesLen) {
    switch (padBytesLen) {
      case 4:
        return ":0400000BFFFFFFFFF5";
      case 12:
        return ":0C00000BFFFFFFFFFFFFFFFFFFFFFFFFF5";
      default:
        var recordData = new Uint8Array(padBytesLen).fill(255);
        return createRecord(0, RecordType.BlockEnd, recordData);
    }
  }
  function paddedDataRecord(padBytesLen) {
    var recordData = new Uint8Array(padBytesLen).fill(255);
    return createRecord(0, RecordType.PaddedData, recordData);
  }
  function convertRecordTo(iHexRecord, recordType) {
    var oRecord = parseRecord(iHexRecord);
    var recordContent = new Uint8Array(oRecord.data.length + 4);
    recordContent[0] = oRecord.data.length;
    recordContent[1] = oRecord.address >> 8;
    recordContent[2] = oRecord.address & 255;
    recordContent[3] = recordType;
    recordContent.set(oRecord.data, 4);
    var recordContentStr = byteArrayToHexStr(recordContent);
    var checksumStr = byteToHexStrFast(calcChecksumByte(recordContent));
    return "" + START_CODE_STR + recordContentStr + checksumStr;
  }
  function convertExtSegToLinAddressRecord(iHexRecord) {
    var segmentAddress = getRecordData(iHexRecord);
    if (segmentAddress.length !== 2 || segmentAddress[0] & 15 || // Only process multiples of 0x1000
    segmentAddress[1] !== 0) {
      throw new Error("Invalid Extended Segment Address record " + iHexRecord);
    }
    var startAddress = segmentAddress[0] << 12;
    return extLinAddressRecord(startAddress);
  }
  function iHexToRecordStrs(iHexStr) {
    var output = iHexStr.replace(/\r/g, "").split("\n");
    return output.filter(Boolean);
  }
  function findDataFieldLength(iHexRecords) {
    var maxDataBytes = 16;
    var maxDataBytesCount = 0;
    for (var _i = 0, iHexRecords_1 = iHexRecords; _i < iHexRecords_1.length; _i++) {
      var record = iHexRecords_1[_i];
      var dataBytesLength = (record.length - MIN_RECORD_STR_LEN) / 2;
      if (dataBytesLength > maxDataBytes) {
        maxDataBytes = dataBytesLength;
        maxDataBytesCount = 0;
      } else if (dataBytesLength === maxDataBytes) {
        maxDataBytesCount++;
      }
      if (maxDataBytesCount > 12) {
        break;
      }
    }
    if (maxDataBytes > RECORD_DATA_MAX_BYTES) {
      throw new Error("Intel Hex record data size is too large: " + maxDataBytes);
    }
    return maxDataBytes;
  }

  // node_modules/@microbit/microbit-universal-hex/dist/esm5/universal-hex.js
  var V1_BOARD_IDS = [39168, 39169];
  var BLOCK_SIZE = 512;
  var microbitBoardId;
  (function(microbitBoardId3) {
    microbitBoardId3[microbitBoardId3["V1"] = 39168] = "V1";
    microbitBoardId3[microbitBoardId3["V2"] = 39171] = "V2";
  })(microbitBoardId || (microbitBoardId = {}));
  function iHexToCustomFormatBlocks(iHexStr, boardId) {
    var replaceDataRecord = !V1_BOARD_IDS.includes(boardId);
    var startRecord = blockStartRecord(boardId);
    var currentExtAddr = extLinAddressRecord(0);
    var extAddrRecordLen = currentExtAddr.length;
    var startRecordLen = startRecord.length;
    var endRecordBaseLen = blockEndRecord(0).length;
    var padRecordBaseLen = paddedDataRecord(0).length;
    var hexRecords = iHexToRecordStrs(iHexStr);
    var recordPaddingCapacity = findDataFieldLength(hexRecords);
    if (!hexRecords.length)
      return "";
    if (isUniversalHexRecords(hexRecords)) {
      throw new Error("Board ID " + boardId + " Hex is already a Universal Hex.");
    }
    var ih = 0;
    var blockLines = [];
    while (ih < hexRecords.length) {
      var blockLen = 0;
      var firstRecordType = getRecordType(hexRecords[ih]);
      if (firstRecordType === RecordType.ExtendedLinearAddress) {
        currentExtAddr = hexRecords[ih];
        ih++;
      } else if (firstRecordType === RecordType.ExtendedSegmentAddress) {
        currentExtAddr = convertExtSegToLinAddressRecord(hexRecords[ih]);
        ih++;
      }
      blockLines.push(currentExtAddr);
      blockLen += extAddrRecordLen + 1;
      blockLines.push(startRecord);
      blockLen += startRecordLen + 1;
      blockLen += endRecordBaseLen + 1;
      var endOfFile = false;
      while (hexRecords[ih] && BLOCK_SIZE >= blockLen + hexRecords[ih].length + 1) {
        var record = hexRecords[ih++];
        var recordType = getRecordType(record);
        if (replaceDataRecord && recordType === RecordType.Data) {
          record = convertRecordTo(record, RecordType.CustomData);
        } else if (recordType === RecordType.ExtendedLinearAddress) {
          currentExtAddr = record;
        } else if (recordType === RecordType.ExtendedSegmentAddress) {
          record = convertExtSegToLinAddressRecord(record);
          currentExtAddr = record;
        } else if (recordType === RecordType.EndOfFile) {
          endOfFile = true;
          break;
        }
        blockLines.push(record);
        blockLen += record.length + 1;
      }
      if (endOfFile) {
        if (ih !== hexRecords.length) {
          if (isMakeCodeForV1HexRecords(hexRecords)) {
            throw new Error("Board ID " + boardId + " Hex is from MakeCode, import this hex into the MakeCode editor to create a Universal Hex.");
          } else {
            throw new Error("EoF record found at record " + ih + " of " + hexRecords.length + " in Board ID " + boardId + " hex");
          }
        }
        blockLines.push(blockEndRecord(0));
        blockLines.push(endOfFileRecord());
      } else {
        while (BLOCK_SIZE - blockLen > recordPaddingCapacity * 2) {
          var record = paddedDataRecord(Math.min((BLOCK_SIZE - blockLen - (padRecordBaseLen + 1)) / 2, recordPaddingCapacity));
          blockLines.push(record);
          blockLen += record.length + 1;
        }
        blockLines.push(blockEndRecord((BLOCK_SIZE - blockLen) / 2));
      }
    }
    blockLines.push("");
    return blockLines.join("\n");
  }
  function iHexToCustomFormatSection(iHexStr, boardId) {
    var sectionLines = [];
    var sectionLen = 0;
    var ih = 0;
    var addRecordLength = function(record2) {
      sectionLen += record2.length + 1;
    };
    var addRecord = function(record2) {
      sectionLines.push(record2);
      addRecordLength(record2);
    };
    var hexRecords = iHexToRecordStrs(iHexStr);
    if (!hexRecords.length)
      return "";
    if (isUniversalHexRecords(hexRecords)) {
      throw new Error("Board ID " + boardId + " Hex is already a Universal Hex.");
    }
    var iHexFirstRecordType = getRecordType(hexRecords[0]);
    if (iHexFirstRecordType === RecordType.ExtendedLinearAddress) {
      addRecord(hexRecords[0]);
      ih++;
    } else if (iHexFirstRecordType === RecordType.ExtendedSegmentAddress) {
      addRecord(convertExtSegToLinAddressRecord(hexRecords[0]));
      ih++;
    } else {
      addRecord(extLinAddressRecord(0));
    }
    addRecord(blockStartRecord(boardId));
    var replaceDataRecord = !V1_BOARD_IDS.includes(boardId);
    var endOfFile = false;
    while (ih < hexRecords.length) {
      var record = hexRecords[ih++];
      var recordType = getRecordType(record);
      if (recordType === RecordType.Data) {
        addRecord(replaceDataRecord ? convertRecordTo(record, RecordType.CustomData) : record);
      } else if (recordType === RecordType.ExtendedSegmentAddress) {
        addRecord(convertExtSegToLinAddressRecord(record));
      } else if (recordType === RecordType.ExtendedLinearAddress) {
        addRecord(record);
      } else if (recordType === RecordType.EndOfFile) {
        endOfFile = true;
        break;
      }
    }
    if (ih !== hexRecords.length) {
      if (isMakeCodeForV1HexRecords(hexRecords)) {
        throw new Error("Board ID " + boardId + " Hex is from MakeCode, import this hex into the MakeCode editor to create a Universal Hex.");
      } else {
        throw new Error("EoF record found at record " + ih + " of " + hexRecords.length + " in Board ID " + boardId + " hex ");
      }
    }
    addRecordLength(blockEndRecord(0));
    var recordNoDataLenChars = paddedDataRecord(0).length + 1;
    var recordDataMaxBytes = findDataFieldLength(hexRecords);
    var paddingCapacityChars = recordDataMaxBytes * 2;
    var charsNeeded = (BLOCK_SIZE - sectionLen % BLOCK_SIZE) % BLOCK_SIZE;
    while (charsNeeded > paddingCapacityChars) {
      var byteLen = charsNeeded - recordNoDataLenChars >> 1;
      var record = paddedDataRecord(Math.min(byteLen, recordDataMaxBytes));
      addRecord(record);
      charsNeeded = (BLOCK_SIZE - sectionLen % BLOCK_SIZE) % BLOCK_SIZE;
    }
    sectionLines.push(blockEndRecord(charsNeeded >> 1));
    if (endOfFile)
      sectionLines.push(endOfFileRecord());
    sectionLines.push("");
    return sectionLines.join("\n");
  }
  function createUniversalHex(hexes, blocks) {
    if (blocks === void 0) {
      blocks = false;
    }
    if (!hexes.length)
      return "";
    var iHexToCustomFormat = blocks ? iHexToCustomFormatBlocks : iHexToCustomFormatSection;
    var eofNlRecord = endOfFileRecord() + "\n";
    var customHexes = [];
    for (var i = 0; i < hexes.length - 1; i++) {
      var customHex = iHexToCustomFormat(hexes[i].hex, hexes[i].boardId);
      if (customHex.endsWith(eofNlRecord)) {
        customHex = customHex.slice(0, customHex.length - eofNlRecord.length);
      }
      customHexes.push(customHex);
    }
    var lastCustomHex = iHexToCustomFormat(hexes[hexes.length - 1].hex, hexes[hexes.length - 1].boardId);
    customHexes.push(lastCustomHex);
    if (!lastCustomHex.endsWith(eofNlRecord)) {
      customHexes.push(eofNlRecord);
    }
    return customHexes.join("");
  }
  function isUniversalHex(hexStr) {
    var elaRecordBeginning = ":02000004";
    if (hexStr.slice(0, elaRecordBeginning.length) !== elaRecordBeginning) {
      return false;
    }
    var i = elaRecordBeginning.length;
    while (hexStr[++i] !== ":" && i < MAX_RECORD_STR_LEN + 3)
      ;
    var blockStartBeginning = ":0400000A";
    if (hexStr.slice(i, i + blockStartBeginning.length) !== blockStartBeginning) {
      return false;
    }
    return true;
  }
  function isUniversalHexRecords(records) {
    return getRecordType(records[0]) === RecordType.ExtendedLinearAddress && getRecordType(records[1]) === RecordType.BlockStart && getRecordType(records[records.length - 1]) === RecordType.EndOfFile;
  }
  function isMakeCodeForV1HexRecords(records) {
    var i = records.indexOf(endOfFileRecord());
    if (i === records.length - 1) {
      while (--i > 0) {
        if (records[i] === extLinAddressRecord(536870912)) {
          return true;
        }
      }
    }
    while (++i < records.length) {
      if (getRecordType(records[i]) === RecordType.OtherData) {
        return true;
      }
      if (records[i] === extLinAddressRecord(536870912)) {
        return true;
      }
    }
    return false;
  }
  function separateUniversalHex(universalHexStr) {
    var records = iHexToRecordStrs(universalHexStr);
    if (!records.length)
      throw new Error("Empty Universal Hex.");
    if (!isUniversalHexRecords(records)) {
      throw new Error("Universal Hex format invalid.");
    }
    var passThroughRecords = [
      RecordType.Data,
      RecordType.EndOfFile,
      RecordType.ExtendedSegmentAddress,
      RecordType.StartSegmentAddress
    ];
    var hexes = {};
    var currentBoardId = 0;
    for (var i = 0; i < records.length; i++) {
      var record = records[i];
      var recordType = getRecordType(record);
      if (passThroughRecords.includes(recordType)) {
        hexes[currentBoardId].hex.push(record);
      } else if (recordType === RecordType.CustomData) {
        hexes[currentBoardId].hex.push(convertRecordTo(record, RecordType.Data));
      } else if (recordType === RecordType.ExtendedLinearAddress) {
        var nextRecord = records[i + 1];
        if (getRecordType(nextRecord) === RecordType.BlockStart) {
          var blockStartData = getRecordData(nextRecord);
          if (blockStartData.length !== 4) {
            throw new Error("Block Start record invalid: " + nextRecord);
          }
          currentBoardId = (blockStartData[0] << 8) + blockStartData[1];
          hexes[currentBoardId] = hexes[currentBoardId] || {
            boardId: currentBoardId,
            lastExtAdd: record,
            hex: [record]
          };
          i++;
        }
        if (hexes[currentBoardId].lastExtAdd !== record) {
          hexes[currentBoardId].lastExtAdd = record;
          hexes[currentBoardId].hex.push(record);
        }
      }
    }
    var returnArray = [];
    Object.keys(hexes).forEach(function(boardId) {
      var hex = hexes[boardId].hex;
      if (hex[hex.length - 1] !== endOfFileRecord()) {
        hex[hex.length] = endOfFileRecord();
      }
      returnArray.push({
        boardId: hexes[boardId].boardId,
        hex: hex.join("\n") + "\n"
      });
    });
    return returnArray;
  }

  // src/micropython-fs-builder.ts
  var import_nrf_intel_hex5 = __toESM(require_intel_hex_browser());

  // src/hex-mem-info.ts
  var import_nrf_intel_hex4 = __toESM(require_intel_hex_browser());

  // src/flash-regions.ts
  var import_nrf_intel_hex2 = __toESM(require_intel_hex_browser());

  // src/hex-map-utils.ts
  function getUint64(intelHexMap, address) {
    const uint64Data = intelHexMap.slicePad(address, 8, 255);
    return new DataView(uint64Data.buffer).getUint32(
      0,
      true
      /* little endian */
    );
  }
  function getUint32(intelHexMap, address) {
    const uint32Data = intelHexMap.slicePad(address, 4, 255);
    return new DataView(uint32Data.buffer).getUint32(
      0,
      true
      /* little endian */
    );
  }
  function getUint16(intelHexMap, address) {
    const uint16Data = intelHexMap.slicePad(address, 2, 255);
    return new DataView(uint16Data.buffer).getUint16(
      0,
      true
      /* little endian */
    );
  }
  function getUint8(intelHexMap, address) {
    const uint16Data = intelHexMap.slicePad(address, 1, 255);
    return uint16Data[0];
  }
  function getString(intelHexMap, address) {
    const memBlock = intelHexMap.slice(address).get(address);
    let iStrEnd = 0;
    while (iStrEnd < memBlock.length && memBlock[iStrEnd] !== 0) iStrEnd++;
    if (iStrEnd === memBlock.length) {
      return "";
    }
    const stringBytes = memBlock.slice(0, iStrEnd);
    return bytesToStr(stringBytes);
  }

  // src/flash-regions.ts
  var MAGIC2_LEN_BYTES = 4;
  var P_SIZE_LOG2_LEN_BYTES = 2;
  var NUM_REG_LEN_BYTES = 2;
  var TABLE_LEN_LEN_BYTES = 2;
  var VERSION_LEN_BYTES = 2;
  var MAGIC_1_LEN_BYTES = 4;
  var RegionHeaderOffset = ((RegionHeaderOffset2) => {
    RegionHeaderOffset2[RegionHeaderOffset2["magic2"] = MAGIC2_LEN_BYTES] = "magic2";
    RegionHeaderOffset2[RegionHeaderOffset2["pageSizeLog2"] = RegionHeaderOffset2.magic2 + P_SIZE_LOG2_LEN_BYTES] = "pageSizeLog2";
    RegionHeaderOffset2[RegionHeaderOffset2["regionCount"] = RegionHeaderOffset2.pageSizeLog2 + NUM_REG_LEN_BYTES] = "regionCount";
    RegionHeaderOffset2[RegionHeaderOffset2["tableLength"] = RegionHeaderOffset2.regionCount + TABLE_LEN_LEN_BYTES] = "tableLength";
    RegionHeaderOffset2[RegionHeaderOffset2["version"] = RegionHeaderOffset2.tableLength + VERSION_LEN_BYTES] = "version";
    RegionHeaderOffset2[RegionHeaderOffset2["magic1"] = RegionHeaderOffset2.version + MAGIC_1_LEN_BYTES] = "magic1";
    return RegionHeaderOffset2;
  })(RegionHeaderOffset || {});
  var REGION_HEADER_MAGIC_1 = 1501507838;
  var REGION_HEADER_MAGIC_2 = 3249657757;
  var REGION_ID_BYTES = 1;
  var REGION_HASH_TYPE_BYTES = 1;
  var REGION_START_PAGE_BYTES = 2;
  var REGION_LEN_BYTES = 4;
  var REGION_HASH_DATA_BYTES = 8;
  var RegionRowOffset = ((RegionRowOffset2) => {
    RegionRowOffset2[RegionRowOffset2["hashData"] = REGION_HASH_DATA_BYTES] = "hashData";
    RegionRowOffset2[RegionRowOffset2["lengthBytes"] = RegionRowOffset2.hashData + REGION_LEN_BYTES] = "lengthBytes";
    RegionRowOffset2[RegionRowOffset2["startPage"] = RegionRowOffset2.lengthBytes + REGION_START_PAGE_BYTES] = "startPage";
    RegionRowOffset2[RegionRowOffset2["hashType"] = RegionRowOffset2.startPage + REGION_HASH_TYPE_BYTES] = "hashType";
    RegionRowOffset2[RegionRowOffset2["id"] = RegionRowOffset2.hashType + REGION_ID_BYTES] = "id";
    return RegionRowOffset2;
  })(RegionRowOffset || {});
  var REGION_ROW_LEN_BYTES = RegionRowOffset.id;
  function getTableHeader(iHexMap, pSize = 1024) {
    let endAddress = 0;
    const magic1ToFind = new Uint8Array(
      new Uint32Array([REGION_HEADER_MAGIC_1]).buffer
    );
    const magic2ToFind = new Uint8Array(
      new Uint32Array([REGION_HEADER_MAGIC_2]).buffer
    );
    const mapEntries = iHexMap.paginate(pSize, 255).entries();
    for (let iter = mapEntries.next(); !iter.done; iter = mapEntries.next()) {
      if (!iter.value) continue;
      const blockByteArray = iter.value[1];
      const subArrayMagic2 = blockByteArray.subarray(-RegionHeaderOffset.magic2);
      if (areUint8ArraysEqual(subArrayMagic2, magic2ToFind) && areUint8ArraysEqual(
        blockByteArray.subarray(
          -RegionHeaderOffset.magic1,
          -(RegionHeaderOffset.magic1 - MAGIC_1_LEN_BYTES)
        ),
        magic1ToFind
      )) {
        const pageStartAddress = iter.value[0];
        endAddress = pageStartAddress + pSize;
        break;
      }
    }
    const version = getUint16(
      iHexMap,
      endAddress - RegionHeaderOffset.version
    );
    const tableLength = getUint16(
      iHexMap,
      endAddress - RegionHeaderOffset.tableLength
    );
    const regionCount = getUint16(
      iHexMap,
      endAddress - RegionHeaderOffset.regionCount
    );
    const pageSizeLog2 = getUint16(
      iHexMap,
      endAddress - RegionHeaderOffset.pageSizeLog2
    );
    const pageSize = Math.pow(2, pageSizeLog2);
    const startAddress = endAddress - RegionHeaderOffset.magic1;
    return {
      pageSizeLog2,
      pageSize,
      regionCount,
      tableLength,
      version,
      endAddress,
      startAddress
    };
  }
  function getRegionRow(iHexMap, rowEndAddress) {
    const id = getUint8(iHexMap, rowEndAddress - RegionRowOffset.id);
    const hashType = getUint8(
      iHexMap,
      rowEndAddress - RegionRowOffset.hashType
    );
    const hashData = getUint64(
      iHexMap,
      rowEndAddress - RegionRowOffset.hashData
    );
    let hashPointerData = "";
    if (hashType === 2 /* pointer */) {
      hashPointerData = getString(iHexMap, hashData & 4294967295);
    }
    const startPage = getUint16(
      iHexMap,
      rowEndAddress - RegionRowOffset.startPage
    );
    const lengthBytes = getUint32(
      iHexMap,
      rowEndAddress - RegionRowOffset.lengthBytes
    );
    return {
      id,
      startPage,
      lengthBytes,
      hashType,
      hashData,
      hashPointerData
    };
  }
  function getHexMapFlashRegionsData(iHexMap) {
    const tableHeader = getTableHeader(iHexMap, 4096);
    const regionRows = {};
    for (let i = 0; i < tableHeader.regionCount; i++) {
      const rowEndAddress = tableHeader.startAddress - i * REGION_ROW_LEN_BYTES;
      const regionRow = getRegionRow(iHexMap, rowEndAddress);
      regionRows[regionRow.id] = regionRow;
    }
    if (!regionRows.hasOwnProperty(2 /* microPython */)) {
      throw new Error(
        "Could not find a MicroPython region in the regions table."
      );
    }
    if (!regionRows.hasOwnProperty(3 /* fs */)) {
      throw new Error(
        "Could not find a File System region in the regions table."
      );
    }
    const runtimeStartAddress = 0;
    let runtimeEndAddress = regionRows[2 /* microPython */].startPage * tableHeader.pageSize + regionRows[2 /* microPython */].lengthBytes;
    runtimeEndAddress = tableHeader.endAddress;
    const uPyVersion = regionRows[2 /* microPython */].hashPointerData;
    const fsStartAddress = regionRows[3 /* fs */].startPage * tableHeader.pageSize;
    const fsEndAddress = fsStartAddress + regionRows[3 /* fs */].lengthBytes;
    return {
      flashPageSize: tableHeader.pageSize,
      flashSize: 512 * 1024,
      flashStartAddress: 0,
      flashEndAddress: 512 * 1024,
      runtimeStartAddress,
      runtimeEndAddress,
      fsStartAddress,
      fsEndAddress,
      uPyVersion,
      deviceVersion: "V2"
    };
  }

  // src/uicr.ts
  var import_nrf_intel_hex3 = __toESM(require_intel_hex_browser());
  var DEVICE_INFO = [
    {
      deviceVersion: "V1",
      magicHeader: 401518716,
      flashSize: 256 * 1024,
      fsEnd: 256 * 1024
    },
    {
      deviceVersion: "V2",
      magicHeader: 1206825084,
      flashSize: 512 * 1024,
      fsEnd: 471040
    }
  ];
  var UICR_START = 268439552;
  var UICR_CUSTOMER_OFFSET = 128;
  var UICR_CUSTOMER_UPY_OFFSET = 64;
  var UICR_UPY_START = UICR_START + UICR_CUSTOMER_OFFSET + UICR_CUSTOMER_UPY_OFFSET;
  var UPY_MAGIC_LEN = 4;
  var UPY_END_MARKER_LEN = 4;
  var UPY_PAGE_SIZE_LEN = 4;
  var UPY_START_PAGE_LEN = 2;
  var UPY_PAGES_USED_LEN = 2;
  var UPY_DELIMITER_LEN = 4;
  var UPY_VERSION_LEN = 4;
  var UPY_REGIONS_TERMINATOR_LEN = 4;
  var MicropythonUicrAddress = ((MicropythonUicrAddress2) => {
    MicropythonUicrAddress2[MicropythonUicrAddress2["MagicValue"] = UICR_UPY_START] = "MagicValue";
    MicropythonUicrAddress2[MicropythonUicrAddress2["EndMarker"] = MicropythonUicrAddress2.MagicValue + UPY_MAGIC_LEN] = "EndMarker";
    MicropythonUicrAddress2[MicropythonUicrAddress2["PageSize"] = MicropythonUicrAddress2.EndMarker + UPY_END_MARKER_LEN] = "PageSize";
    MicropythonUicrAddress2[MicropythonUicrAddress2["StartPage"] = MicropythonUicrAddress2.PageSize + UPY_PAGE_SIZE_LEN] = "StartPage";
    MicropythonUicrAddress2[MicropythonUicrAddress2["PagesUsed"] = MicropythonUicrAddress2.StartPage + UPY_START_PAGE_LEN] = "PagesUsed";
    MicropythonUicrAddress2[MicropythonUicrAddress2["Delimiter"] = MicropythonUicrAddress2.PagesUsed + UPY_PAGES_USED_LEN] = "Delimiter";
    MicropythonUicrAddress2[MicropythonUicrAddress2["VersionLocation"] = MicropythonUicrAddress2.Delimiter + UPY_DELIMITER_LEN] = "VersionLocation";
    MicropythonUicrAddress2[MicropythonUicrAddress2["RegionsTerminator"] = MicropythonUicrAddress2.VersionLocation + UPY_REGIONS_TERMINATOR_LEN] = "RegionsTerminator";
    MicropythonUicrAddress2[MicropythonUicrAddress2["End"] = MicropythonUicrAddress2.RegionsTerminator + UPY_VERSION_LEN] = "End";
    return MicropythonUicrAddress2;
  })(MicropythonUicrAddress || {});
  function confirmMagicValue(intelHexMap) {
    const readMagicHeader = getMagicValue(intelHexMap);
    for (const device of DEVICE_INFO) {
      if (device.magicHeader === readMagicHeader) {
        return true;
      }
    }
    return false;
  }
  function getMagicValue(intelHexMap) {
    return getUint32(intelHexMap, MicropythonUicrAddress.MagicValue);
  }
  function getDeviceVersion(intelHexMap) {
    const readMagicHeader = getMagicValue(intelHexMap);
    for (const device of DEVICE_INFO) {
      if (device.magicHeader === readMagicHeader) {
        return device.deviceVersion;
      }
    }
    throw new Error("Cannot find device version, unknown UICR Magic value");
  }
  function getFlashSize(intelHexMap) {
    const readMagicHeader = getMagicValue(intelHexMap);
    for (const device of DEVICE_INFO) {
      if (device.magicHeader === readMagicHeader) {
        return device.flashSize;
      }
    }
    throw new Error("Cannot find flash size, unknown UICR Magic value");
  }
  function getFsEndAddress(intelHexMap) {
    const readMagicHeader = getMagicValue(intelHexMap);
    for (const device of DEVICE_INFO) {
      if (device.magicHeader === readMagicHeader) {
        return device.fsEnd;
      }
    }
    throw new Error("Cannot find fs end address, unknown UICR Magic value");
  }
  function getPageSize(intelHexMap) {
    const pageSize = getUint32(
      intelHexMap,
      MicropythonUicrAddress.PageSize
    );
    return Math.pow(2, pageSize);
  }
  function getStartPage(intelHexMap) {
    return getUint16(intelHexMap, MicropythonUicrAddress.StartPage);
  }
  function getPagesUsed(intelHexMap) {
    return getUint16(intelHexMap, MicropythonUicrAddress.PagesUsed);
  }
  function getVersionLocation(intelHexMap) {
    return getUint32(
      intelHexMap,
      MicropythonUicrAddress.VersionLocation
    );
  }
  function getHexMapUicrData(intelHexMap) {
    const uicrMap = intelHexMap.slice(UICR_UPY_START);
    if (!confirmMagicValue(uicrMap)) {
      throw new Error("Could not find valid MicroPython UICR data.");
    }
    const flashPageSize = getPageSize(uicrMap);
    const flashSize = getFlashSize(uicrMap);
    const startPage = getStartPage(uicrMap);
    const flashStartAddress = startPage * flashPageSize;
    const flashEndAddress = flashStartAddress + flashSize;
    const pagesUsed = getPagesUsed(uicrMap);
    const runtimeEndAddress = pagesUsed * flashPageSize;
    const versionAddress = getVersionLocation(uicrMap);
    const uPyVersion = getString(intelHexMap, versionAddress);
    const deviceVersion = getDeviceVersion(uicrMap);
    const fsEndAddress = getFsEndAddress(uicrMap);
    return {
      flashPageSize,
      flashSize,
      flashStartAddress,
      flashEndAddress,
      runtimeStartAddress: flashStartAddress,
      runtimeEndAddress,
      fsStartAddress: runtimeEndAddress,
      fsEndAddress,
      uicrStartAddress: MicropythonUicrAddress.MagicValue,
      uicrEndAddress: MicropythonUicrAddress.End,
      uPyVersion,
      deviceVersion
    };
  }

  // src/hex-mem-info.ts
  function getHexMapDeviceMemInfo(intelHexMap) {
    let errorMsg = "";
    try {
      return getHexMapUicrData(intelHexMap);
    } catch (err) {
      errorMsg += err.message + "\n";
    }
    try {
      return getHexMapFlashRegionsData(intelHexMap);
    } catch (err) {
      throw new Error(errorMsg + err.message);
    }
  }
  function getIntelHexDeviceMemInfo(intelHex) {
    return getHexMapDeviceMemInfo(import_nrf_intel_hex4.default.fromHex(intelHex));
  }

  // src/micropython-fs-builder.ts
  var CHUNK_LEN = 128;
  var CHUNK_MARKER_LEN = 1;
  var CHUNK_TAIL_LEN = 1;
  var CHUNK_DATA_LEN = CHUNK_LEN - CHUNK_MARKER_LEN - CHUNK_TAIL_LEN;
  var CHUNK_HEADER_END_OFFSET_LEN = 1;
  var CHUNK_HEADER_NAME_LEN = 1;
  var MAX_FILENAME_LENGTH = 120;
  var MAX_NUMBER_OF_CHUNKS = 256 - 4;
  function createMpFsBuilderCache(originalIntelHex) {
    const originalMemMap = import_nrf_intel_hex5.default.fromHex(originalIntelHex);
    const deviceMem = getHexMapDeviceMemInfo(originalMemMap);
    const uPyIntelHex = originalMemMap.slice(
      deviceMem.runtimeStartAddress,
      deviceMem.runtimeEndAddress - deviceMem.runtimeStartAddress
    ).asHexString().replace(":00000001FF", "");
    return {
      originalIntelHex,
      originalMemMap,
      uPyIntelHex,
      uPyEndAddress: deviceMem.runtimeEndAddress,
      fsSize: getMemMapFsSize(originalMemMap)
    };
  }
  function getFreeChunks(intelHexMap) {
    const freeChunks = [];
    const startAddress = getStartAddress(intelHexMap);
    const endAddress = getLastPageAddress(intelHexMap);
    let chunkAddr = startAddress;
    let chunkIndex = 1;
    while (chunkAddr < endAddress) {
      const marker = intelHexMap.slicePad(chunkAddr, 1, 255 /* Unused */)[0];
      if (marker === 255 /* Unused */ || marker === 0 /* Freed */) {
        freeChunks.push(chunkIndex);
      }
      chunkIndex++;
      chunkAddr += CHUNK_LEN;
    }
    return freeChunks;
  }
  function getStartAddress(intelHexMap) {
    const deviceMem = getHexMapDeviceMemInfo(intelHexMap);
    const fsMaxSize = CHUNK_LEN * MAX_NUMBER_OF_CHUNKS;
    const startAddressForMaxFs = getEndAddress(intelHexMap) - fsMaxSize;
    const startAddress = Math.max(deviceMem.fsStartAddress, startAddressForMaxFs);
    if (startAddress % deviceMem.flashPageSize) {
      throw new Error(
        "File system start address from UICR does not align with flash page size."
      );
    }
    return startAddress;
  }
  function getEndAddress(intelHexMap) {
    const deviceMem = getHexMapDeviceMemInfo(intelHexMap);
    let endAddress = deviceMem.fsEndAddress;
    if (deviceMem.deviceVersion === "V1") {
      if (isAppendedScriptPresent(intelHexMap)) {
        endAddress = 253952 /* StartAdd */;
      }
      endAddress -= deviceMem.flashPageSize;
    }
    return endAddress;
  }
  function getLastPageAddress(intelHexMap) {
    const deviceMem = getHexMapDeviceMemInfo(intelHexMap);
    return getEndAddress(intelHexMap) - deviceMem.flashPageSize;
  }
  function setPersistentPage(intelHexMap) {
    intelHexMap.set(
      getLastPageAddress(intelHexMap),
      new Uint8Array([253 /* PersistentData */])
    );
  }
  function chuckIndexAddress(intelHexMap, chunkIndex) {
    return getStartAddress(intelHexMap) + (chunkIndex - 1) * CHUNK_LEN;
  }
  var FsFile = class {
    _filename;
    _filenameBytes;
    _dataBytes;
    _fsDataBytes;
    /**
     * Create a file.
     *
     * @param filename - Name for the file.
     * @param data - Byte array with the file data.
     */
    constructor(filename, data) {
      this._filename = filename;
      this._filenameBytes = strToBytes(filename);
      if (this._filenameBytes.length > MAX_FILENAME_LENGTH) {
        throw new Error(
          `File name "${filename}" is too long (max ${MAX_FILENAME_LENGTH} characters).`
        );
      }
      this._dataBytes = data;
      const fileHeader = this._generateFileHeaderBytes();
      this._fsDataBytes = new Uint8Array(
        fileHeader.length + this._dataBytes.length + 1
      );
      this._fsDataBytes.set(fileHeader, 0);
      this._fsDataBytes.set(this._dataBytes, fileHeader.length);
      this._fsDataBytes[this._fsDataBytes.length - 1] = 255;
    }
    /**
     * Generate an array of file system chunks for all this file content.
     *
     * @throws {Error} When there are not enough chunks available.
     *
     * @param freeChunks - List of available chunks to use.
     * @returns An array of byte arrays, one item per chunk.
     */
    getFsChunks(freeChunks) {
      const chunks = [];
      let freeChunksIndex = 0;
      let dataIndex = 0;
      let chunk = new Uint8Array(CHUNK_LEN).fill(255);
      chunk[0 /* Marker */] = 254 /* FileStart */;
      let loopEnd = Math.min(this._fsDataBytes.length, CHUNK_DATA_LEN);
      for (let i = 0; i < loopEnd; i++, dataIndex++) {
        chunk[CHUNK_MARKER_LEN + i] = this._fsDataBytes[dataIndex];
      }
      chunks.push(chunk);
      while (dataIndex < this._fsDataBytes.length) {
        freeChunksIndex++;
        if (freeChunksIndex >= freeChunks.length) {
          throw new Error(`Not enough space for the ${this._filename} file.`);
        }
        const previousChunk = chunks[chunks.length - 1];
        previousChunk[127 /* Tail */] = freeChunks[freeChunksIndex];
        chunk = new Uint8Array(CHUNK_LEN).fill(255);
        chunk[0 /* Marker */] = freeChunks[freeChunksIndex - 1];
        loopEnd = Math.min(this._fsDataBytes.length - dataIndex, CHUNK_DATA_LEN);
        for (let i = 0; i < loopEnd; i++, dataIndex++) {
          chunk[CHUNK_MARKER_LEN + i] = this._fsDataBytes[dataIndex];
        }
        chunks.push(chunk);
      }
      return chunks;
    }
    /**
     * Generate a single byte array with the filesystem data for this file.
     *
     * @param freeChunks - List of available chunks to use.
     * @returns A byte array with the data to go straight into flash.
     */
    getFsBytes(freeChunks) {
      const chunks = this.getFsChunks(freeChunks);
      const chunksLen = chunks.length * CHUNK_LEN;
      const fileFsBytes = new Uint8Array(chunksLen);
      for (let i = 0; i < chunks.length; i++) {
        fileFsBytes.set(chunks[i], CHUNK_LEN * i);
      }
      return fileFsBytes;
    }
    /**
     * @returns Size, in bytes, of how much space the file takes in the filesystem
     *     flash memory.
     */
    getFsFileSize() {
      const chunksUsed = Math.ceil(this._fsDataBytes.length / CHUNK_DATA_LEN);
      return chunksUsed * CHUNK_LEN;
    }
    /**
     * Generates a byte array for the file header as expected by the MicroPython
     * file system.
     *
     * @return Byte array with the header data.
     */
    _generateFileHeaderBytes() {
      const headerSize = CHUNK_HEADER_END_OFFSET_LEN + CHUNK_HEADER_NAME_LEN + this._filenameBytes.length;
      const endOffset = (headerSize + this._dataBytes.length) % CHUNK_DATA_LEN;
      const fileNameOffset = headerSize - this._filenameBytes.length;
      const headerBytes = new Uint8Array(headerSize);
      headerBytes[1 /* EndOffset */ - 1] = endOffset;
      headerBytes[2 /* NameLength */ - 1] = this._filenameBytes.length;
      for (let i = fileNameOffset; i < headerSize; ++i) {
        headerBytes[i] = this._filenameBytes[i - fileNameOffset];
      }
      return headerBytes;
    }
  };
  function calculateFileSize(filename, data) {
    const file = new FsFile(filename, data);
    return file.getFsFileSize();
  }
  function addMemMapFile(intelHexMap, filename, data) {
    if (!filename) throw new Error("File has to have a file name.");
    if (!data.length) throw new Error(`File ${filename} has to contain data.`);
    const freeChunks = getFreeChunks(intelHexMap);
    if (freeChunks.length === 0) {
      throw new Error("There is no storage space left.");
    }
    const chunksStartAddress = chuckIndexAddress(intelHexMap, freeChunks[0]);
    const fsFile = new FsFile(filename, data);
    const fileFsBytes = fsFile.getFsBytes(freeChunks);
    intelHexMap.set(chunksStartAddress, fileFsBytes);
    setPersistentPage(intelHexMap);
  }
  function addIntelHexFiles(intelHex, files, returnBytes = false) {
    let intelHexMap;
    if (typeof intelHex === "string") {
      intelHexMap = import_nrf_intel_hex5.default.fromHex(intelHex);
    } else {
      intelHexMap = intelHex.clone();
    }
    const deviceMem = getHexMapDeviceMemInfo(intelHexMap);
    Object.keys(files).forEach((filename) => {
      addMemMapFile(intelHexMap, filename, files[filename]);
    });
    return returnBytes ? intelHexMap.slicePad(0, deviceMem.flashSize) : intelHexMap.asHexString() + "\n";
  }
  function generateHexWithFiles(cache, files) {
    const memMapWithFiles = cache.originalMemMap.clone();
    Object.keys(files).forEach((filename) => {
      addMemMapFile(memMapWithFiles, filename, files[filename]);
    });
    return cache.uPyIntelHex + memMapWithFiles.slice(cache.uPyEndAddress).asHexString() + "\n";
  }
  function getIntelHexFiles(intelHex) {
    let hexMap;
    if (typeof intelHex === "string") {
      hexMap = import_nrf_intel_hex5.default.fromHex(intelHex);
    } else {
      hexMap = intelHex.clone();
    }
    const startAddress = getStartAddress(hexMap);
    const endAddress = getLastPageAddress(hexMap);
    const usedChunks = {};
    const startChunkIndexes = [];
    let chunkAddr = startAddress;
    let chunkIndex = 1;
    while (chunkAddr < endAddress) {
      const chunk = hexMap.slicePad(chunkAddr, CHUNK_LEN, 255 /* Unused */);
      const marker = chunk[0];
      if (marker !== 255 /* Unused */ && marker !== 0 /* Freed */ && marker !== 253 /* PersistentData */) {
        usedChunks[chunkIndex] = chunk;
        if (marker === 254 /* FileStart */) {
          startChunkIndexes.push(chunkIndex);
        }
      }
      chunkIndex++;
      chunkAddr += CHUNK_LEN;
    }
    const files = {};
    for (const startChunkIndex of startChunkIndexes) {
      const startChunk = usedChunks[startChunkIndex];
      const endChunkOffset = startChunk[1 /* EndOffset */];
      const filenameLen = startChunk[2 /* NameLength */];
      let chunkDataStart = 3 + filenameLen;
      const filename = bytesToStr(startChunk.slice(3, chunkDataStart));
      if (files.hasOwnProperty(filename)) {
        throw new Error(`Found multiple files named: ${filename}.`);
      }
      files[filename] = new Uint8Array(0);
      let currentChunk = startChunk;
      let currentIndex = startChunkIndex;
      let iterations = Object.keys(usedChunks).length + 1;
      while (iterations--) {
        const nextIndex = currentChunk[127 /* Tail */];
        if (nextIndex === 255 /* Unused */) {
          files[filename] = concatUint8Array(
            files[filename],
            currentChunk.slice(chunkDataStart, 1 + endChunkOffset)
          );
          break;
        } else {
          files[filename] = concatUint8Array(
            files[filename],
            currentChunk.slice(chunkDataStart, 127 /* Tail */)
          );
        }
        const nextChunk = usedChunks[nextIndex];
        if (!nextChunk) {
          throw new Error(
            `Chunk ${currentIndex} points to unused index ${nextIndex}.`
          );
        }
        if (nextChunk[0 /* Marker */] !== currentIndex) {
          throw new Error(
            `Chunk index ${nextIndex} did not link to previous chunk index ${currentIndex}.`
          );
        }
        currentChunk = nextChunk;
        currentIndex = nextIndex;
        chunkDataStart = 1;
      }
      if (iterations <= 0) {
        throw new Error("Malformed file chunks did not link correctly.");
      }
    }
    return files;
  }
  function getMemMapFsSize(intelHexMap) {
    const deviceMem = getHexMapDeviceMemInfo(intelHexMap);
    const startAddress = getStartAddress(intelHexMap);
    const endAddress = getEndAddress(intelHexMap);
    return endAddress - startAddress - deviceMem.flashPageSize;
  }

  // src/simple-file.ts
  var SimpleFile = class {
    filename;
    _dataBytes;
    /**
     * Create a SimpleFile.
     *
     * @throws {Error} When an invalid filename is provided.
     * @throws {Error} When invalid file data is provided.
     *
     * @param filename - Name for the file.
     * @param data - String or byte array with the file data.
     */
    constructor(filename, data) {
      if (!filename) {
        throw new Error("File was not provided a valid filename.");
      }
      if (!data) {
        throw new Error(`File ${filename} does not have valid content.`);
      }
      this.filename = filename;
      if (typeof data === "string") {
        this._dataBytes = strToBytes(data);
      } else if (data instanceof Uint8Array) {
        this._dataBytes = data;
      } else {
        throw new Error("File data type must be a string or Uint8Array.");
      }
    }
    getText() {
      return bytesToStr(this._dataBytes);
    }
    getBytes() {
      return this._dataBytes;
    }
  };

  // src/micropython-fs-hex.ts
  var microbitBoardId2 = microbitBoardId;
  var MicropythonFsHex = class {
    _uPyFsBuilderCache = [];
    _files = {};
    _storageSize = 0;
    /**
     * File System manager constructor.
     *
     * At the moment it needs a MicroPython hex string without files included.
     * Multiple MicroPython images can be provided to generate a Universal Hex.
     *
     * @throws {Error} When any of the input iHex contains filesystem files.
     * @throws {Error} When any of the input iHex is not a valid MicroPython hex.
     *
     * @param intelHex - MicroPython Intel Hex string or an array of Intel Hex
     *    strings with their respective board IDs.
     */
    constructor(intelHex, { maxFsSize = 0 } = {}) {
      const hexWithIdArray = Array.isArray(intelHex) ? intelHex : [
        {
          hex: intelHex,
          boardId: 0
        }
      ];
      let minFsSize = Infinity;
      hexWithIdArray.forEach((hexWithId) => {
        if (!hexWithId.hex) {
          throw new Error("Invalid MicroPython hex.");
        }
        const builderCache = createMpFsBuilderCache(hexWithId.hex);
        const thisBuilderCache = {
          originalIntelHex: builderCache.originalIntelHex,
          originalMemMap: builderCache.originalMemMap,
          uPyEndAddress: builderCache.uPyEndAddress,
          uPyIntelHex: builderCache.uPyIntelHex,
          fsSize: builderCache.fsSize,
          boardId: hexWithId.boardId
        };
        this._uPyFsBuilderCache.push(thisBuilderCache);
        minFsSize = Math.min(minFsSize, thisBuilderCache.fsSize);
      });
      this.setStorageSize(maxFsSize || minFsSize);
      this._uPyFsBuilderCache.forEach((builderCache) => {
        const hexFiles = getIntelHexFiles(builderCache.originalMemMap);
        if (Object.keys(hexFiles).length) {
          throw new Error(
            "There are files in the MicropythonFsHex constructor hex file input."
          );
        }
      });
    }
    /**
     * Create a new file and add it to the file system.
     *
     * @throws {Error} When the file already exists.
     * @throws {Error} When an invalid filename is provided.
     * @throws {Error} When invalid file data is provided.
     *
     * @param filename - Name for the file.
     * @param content - File content to write.
     */
    create(filename, content) {
      if (this.exists(filename)) {
        throw new Error("File already exists.");
      }
      this.write(filename, content);
    }
    /**
     * Write a file into the file system. Overwrites a previous file with the
     * same name.
     *
     * @throws {Error} When an invalid filename is provided.
     * @throws {Error} When invalid file data is provided.
     *
     * @param filename - Name for the file.
     * @param content - File content to write.
     */
    write(filename, content) {
      this._files[filename] = new SimpleFile(filename, content);
    }
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    append(filename, content) {
      if (!filename) {
        throw new Error("Invalid filename.");
      }
      if (!this.exists(filename)) {
        throw new Error(`File "${filename}" does not exist.`);
      }
      throw new Error("Append operation not yet implemented.");
    }
    /**
     * Read the text from a file.
     *
     * @throws {Error} When invalid file name is provided.
     * @throws {Error} When file is not in the file system.
     *
     * @param filename - Name of the file to read.
     * @returns Text from the file.
     */
    read(filename) {
      if (!filename) {
        throw new Error("Invalid filename.");
      }
      if (!this.exists(filename)) {
        throw new Error(`File "${filename}" does not exist.`);
      }
      return this._files[filename].getText();
    }
    /**
     * Read the bytes from a file.
     *
     * @throws {Error} When invalid file name is provided.
     * @throws {Error} When file is not in the file system.
     *
     * @param filename - Name of the file to read.
     * @returns Byte array from the file.
     */
    readBytes(filename) {
      if (!filename) {
        throw new Error("Invalid filename.");
      }
      if (!this.exists(filename)) {
        throw new Error(`File "${filename}" does not exist.`);
      }
      return this._files[filename].getBytes();
    }
    /**
     * Delete a file from the file system.
     *
     * @throws {Error} When invalid file name is provided.
     * @throws {Error} When the file doesn't exist.
     *
     * @param filename - Name of the file to delete.
     */
    remove(filename) {
      if (!filename) {
        throw new Error("Invalid filename.");
      }
      if (!this.exists(filename)) {
        throw new Error(`File "${filename}" does not exist.`);
      }
      delete this._files[filename];
    }
    /**
     * Check if a file is already present in the file system.
     *
     * @param filename - Name for the file to check.
     * @returns True if it exists, false otherwise.
     */
    exists(filename) {
      return this._files.hasOwnProperty(filename);
    }
    /**
     * Returns the size of a file in bytes.
     *
     * @throws {Error} When invalid file name is provided.
     * @throws {Error} When the file doesn't exist.
     *
     * @param filename - Name for the file to check.
     * @returns Size file size in bytes.
     */
    size(filename) {
      if (!filename) {
        throw new Error(`Invalid filename: ${filename}`);
      }
      if (!this.exists(filename)) {
        throw new Error(`File "${filename}" does not exist.`);
      }
      return calculateFileSize(
        this._files[filename].filename,
        this._files[filename].getBytes()
      );
    }
    /**
     * @returns A list all the files in the file system.
     */
    ls() {
      const files = [];
      Object.values(this._files).forEach((value) => files.push(value.filename));
      return files;
    }
    /**
     * Sets a storage size limit. Must be smaller than available space in
     * MicroPython.
     *
     * @param {number} size - Size in bytes for the filesystem.
     */
    setStorageSize(size) {
      let minFsSize = Infinity;
      this._uPyFsBuilderCache.forEach((builderCache) => {
        minFsSize = Math.min(minFsSize, builderCache.fsSize);
      });
      if (size > minFsSize) {
        throw new Error(
          "Storage size limit provided is larger than size available in the MicroPython hex."
        );
      }
      this._storageSize = size;
    }
    /**
     * The available filesystem total size either calculated by the MicroPython
     * hex or the max storage size limit has been set.
     *
     * @returns Size of the filesystem in bytes.
     */
    getStorageSize() {
      return this._storageSize;
    }
    /**
     * @returns The total number of bytes currently used by files in the file system.
     */
    getStorageUsed() {
      return Object.values(this._files).reduce(
        (accumulator, current) => accumulator + this.size(current.filename),
        0
      );
    }
    /**
     * @returns The remaining storage of the file system in bytes.
     */
    getStorageRemaining() {
      return this.getStorageSize() - this.getStorageUsed();
    }
    /**
     * Read the files included in a MicroPython hex string and add them to this
     * instance.
     *
     * @throws {Error} When there are no files to import in the hex.
     * @throws {Error} When there is a problem reading the files from the hex.
     * @throws {Error} When a filename already exists in this instance (all other
     *     files are still imported).
     *
     * @param intelHex - MicroPython hex string with files.
     * @param overwrite - Flag to overwrite existing files in this instance.
     * @param formatFirst - Erase all the previous files before importing. It only
     *     erases the files after there are no error during hex file parsing.
     * @returns A filename list of added files.
     */
    importFilesFromIntelHex(intelHex, { overwrite = false, formatFirst = false } = {}) {
      const files = getIntelHexFiles(intelHex);
      if (!Object.keys(files).length) {
        throw new Error("Intel Hex does not have any files to import");
      }
      if (formatFirst) {
        this._files = {};
      }
      const existingFiles = [];
      Object.keys(files).forEach((filename) => {
        if (!overwrite && this.exists(filename)) {
          existingFiles.push(filename);
        } else {
          this.write(filename, files[filename]);
        }
      });
      if (existingFiles.length) {
        throw new Error(`Files "${existingFiles}" from hex already exists.`);
      }
      return Object.keys(files);
    }
    /**
     * Read the files included in a MicroPython Universal Hex string and add them
     * to this instance.
     *
     * @throws {Error} When there are no files to import from one of the hex.
     * @throws {Error} When the files in the individual hex are different.
     * @throws {Error} When there is a problem reading files from one of the hex.
     * @throws {Error} When a filename already exists in this instance (all other
     *     files are still imported).
     *
     * @param universalHex - MicroPython Universal Hex string with files.
     * @param overwrite - Flag to overwrite existing files in this instance.
     * @param formatFirst - Erase all the previous files before importing. It only
     *     erases the files after there are no error during hex file parsing.
     * @returns A filename list of added files.
     */
    importFilesFromUniversalHex(universalHex, { overwrite = false, formatFirst = false } = {}) {
      if (!isUniversalHex(universalHex)) {
        throw new Error("Universal Hex provided is invalid.");
      }
      const hexWithIds = separateUniversalHex(universalHex);
      const allFileGroups = [];
      hexWithIds.forEach((hexWithId) => {
        const fileGroup = getIntelHexFiles(hexWithId.hex);
        if (!Object.keys(fileGroup).length) {
          throw new Error(
            `Hex with ID ${hexWithId.boardId} from Universal Hex does not have any files to import`
          );
        }
        allFileGroups.push(fileGroup);
      });
      allFileGroups.forEach((fileGroup) => {
        const compareFileGroups = allFileGroups.filter((v) => v !== fileGroup);
        for (const [fileName, fileContent] of Object.entries(fileGroup)) {
          compareFileGroups.forEach((compareGroup) => {
            if (!compareGroup.hasOwnProperty(fileName) || !areUint8ArraysEqual(compareGroup[fileName], fileContent)) {
              throw new Error(
                "Mismatch in the different Hexes inside the Universal Hex"
              );
            }
          });
        }
      });
      const files = allFileGroups[0];
      if (formatFirst) {
        this._files = {};
      }
      const existingFiles = [];
      Object.keys(files).forEach((filename) => {
        if (!overwrite && this.exists(filename)) {
          existingFiles.push(filename);
        } else {
          this.write(filename, files[filename]);
        }
      });
      if (existingFiles.length) {
        throw new Error(`Files "${existingFiles}" from hex already exists.`);
      }
      return Object.keys(files);
    }
    /**
     * Read the files included in a MicroPython Universal or Intel Hex string and
     * add them to this instance.
     *
     * @throws {Error} When there are no files to import from the hex.
     * @throws {Error} When in the Universal Hex the files of the individual hexes
     *    are different.
     * @throws {Error} When there is a problem reading files from one of the hex.
     * @throws {Error} When a filename already exists in this instance (all other
     *     files are still imported).
     *
     * @param hexStr - MicroPython Intel or Universal Hex string with files.
     * @param overwrite - Flag to overwrite existing files in this instance.
     * @param formatFirst - Erase all the previous files before importing. It only
     *     erases the files after there are no error during hex file parsing.
     * @returns A filename list of added files.
     */
    importFilesFromHex(hexStr, options = {}) {
      return isUniversalHex(hexStr) ? this.importFilesFromUniversalHex(hexStr, options) : this.importFilesFromIntelHex(hexStr, options);
    }
    /**
     * Generate a new copy of the MicroPython Intel Hex with the files in the
     * filesystem included.
     *
     * @throws {Error} When a file doesn't have any data.
     * @throws {Error} When there are issues calculating file system boundaries.
     * @throws {Error} When there is no space left for a file.
     * @throws {Error} When the board ID is not found.
     * @throws {Error} When there are multiple MicroPython hexes and board ID is
     *    not provided.
     *
     * @param boardId - When multiple MicroPython hex files are provided select
     *    one via this argument.
     *
     * @returns A new string with MicroPython and the filesystem included.
     */
    getIntelHex(boardId) {
      if (this.getStorageRemaining() < 0) {
        throw new Error("There is no storage space left.");
      }
      const files = {};
      Object.values(this._files).forEach((file) => {
        files[file.filename] = file.getBytes();
      });
      if (boardId === void 0) {
        if (this._uPyFsBuilderCache.length === 1) {
          return generateHexWithFiles(this._uPyFsBuilderCache[0], files);
        } else {
          throw new Error(
            "The Board ID must be specified if there are multiple MicroPythons."
          );
        }
      }
      for (const builderCache of this._uPyFsBuilderCache) {
        if (builderCache.boardId === boardId) {
          return generateHexWithFiles(builderCache, files);
        }
      }
      throw new Error("Board ID requested not found.");
    }
    /**
     * Generate a byte array of the MicroPython and filesystem data.
     *
     * @throws {Error} When a file doesn't have any data.
     * @throws {Error} When there are issues calculating file system boundaries.
     * @throws {Error} When there is no space left for a file.
     * @throws {Error} When the board ID is not found.
     * @throws {Error} When there are multiple MicroPython hexes and board ID is
     *    not provided.
     *
     * @param boardId - When multiple MicroPython hex files are provided select
     *    one via this argument.
     *
     * @returns A Uint8Array with MicroPython and the filesystem included.
     */
    getIntelHexBytes(boardId) {
      if (this.getStorageRemaining() < 0) {
        throw new Error("There is no storage space left.");
      }
      const files = {};
      Object.values(this._files).forEach((file) => {
        files[file.filename] = file.getBytes();
      });
      if (boardId === void 0) {
        if (this._uPyFsBuilderCache.length === 1) {
          return addIntelHexFiles(
            this._uPyFsBuilderCache[0].originalMemMap,
            files,
            true
          );
        } else {
          throw new Error(
            "The Board ID must be specified if there are multiple MicroPythons."
          );
        }
      }
      for (const builderCache of this._uPyFsBuilderCache) {
        if (builderCache.boardId === boardId) {
          return addIntelHexFiles(
            builderCache.originalMemMap,
            files,
            true
          );
        }
      }
      throw new Error("Board ID requested not found.");
    }
    /**
     * Generate a new copy of a MicroPython Universal Hex with the files in the
     * filesystem included.
     *
     * @throws {Error} When a file doesn't have any data.
     * @throws {Error} When there are issues calculating file system boundaries.
     * @throws {Error} When there is no space left for a file.
     * @throws {Error} When this method is called without having multiple
     *    MicroPython hexes.
     *
     * @returns A new Universal Hex string with MicroPython and filesystem.
     */
    getUniversalHex() {
      if (this._uPyFsBuilderCache.length === 1) {
        throw new Error(
          "MicropythonFsHex constructor must have more than one MicroPython Intel Hex to generate a Universal Hex."
        );
      }
      const iHexWithIds = [];
      this._uPyFsBuilderCache.forEach((builderCache) => {
        iHexWithIds.push({
          hex: this.getIntelHex(builderCache.boardId),
          boardId: builderCache.boardId
        });
      });
      return createUniversalHex(iHexWithIds);
    }
  };
  return __toCommonJS(index_exports);
})();
