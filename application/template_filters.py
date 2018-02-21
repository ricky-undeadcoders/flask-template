from middleware import (split_datetime, pretty_date, pretty_time, clean_javascript_text, format_error_message, slugify,
                        jsonify, remove_whitespace)

template_filters = [split_datetime, pretty_date, pretty_time, clean_javascript_text, format_error_message, slugify,
                    jsonify, remove_whitespace]
