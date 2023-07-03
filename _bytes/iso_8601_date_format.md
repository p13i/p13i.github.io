---
layout: post
title: "ISO 8601 `Date` string formatting"
programming_language: Java
date: 2020-04-06
---

# `DateUtils.java`

Conforms to the ISO specification for a UTC timestamp in the format like `2023-07-03T08:11:22Z`.

```java
package io.p13i.ra.utils;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

/**
 * Utilities for formatting dates
 */
public class DateUtils {

    public static final String YEAR_FORMAT = "yyyy";
    public static final String MONTH_FORMAT = "MM";
    public static final String DAY_FORMAT = "dd";
    public static final String DAY_OF_WEEK_FORMAT = "EEE";  // unused
    public static final String HOUR_FORMAT = "HH";
    public static final String MINUTE_FORMAT = "mm";
    public static final String SECOND_FORMAT = "ss";

    private static final String TIMESTAMP_FORMAT = "yyyy-MM-dd'T'HH:mm:ssZ";

    /**
     * Formats a date
     *
     * @param date    the date to format
     * @param pattern the pattern to use
     * @return the formatted date
     */
    public static String formatDate(Date date, final String pattern) {
        return new SimpleDateFormat(pattern).format(date);
    }

    /**
     * Gets the current time
     *
     * @return the current time as a date
     */
    public static Date now() {
        return Calendar.getInstance().getTime();
    }

    /**
     * Gets the timestamp of the given date
     *
     * @param date the date
     * @return a formatted string timestamp
     */
    public static String timestampOf(Date date) {
        if (date == null) {
            return null;
        }
        return formatDate(date, TIMESTAMP_FORMAT);
    }

    /**
     * Parses the given timestamp string based on the TIMESTAMP_FORMAT
     *
     * @param timestamp the timestamp string
     * @return a Date or null if parsing failed or if the provided timestamp is null or whitespace
     */
    public static Date parseTimestamp(String timestamp) {
        if (timestamp == null) {
            return null;
        }
        return new SimpleDateFormat(TIMESTAMP_FORMAT).parse(timestamp);
    }
}
```
