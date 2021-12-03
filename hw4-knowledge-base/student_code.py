import read, copy
from util import *
from logical_classes import *

verbose = 0


class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact):
        """Retract a fact from the KB

        Args:
            fact (Fact) - Fact to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact])
        ####################################################
        # Student code goes here
        # First we have to check if the length of the supported by fact is not 0, if it is we return None
        if len(fact.supported_by) != 0:
            return None
        # Secondly, We have to check if the given parameter fact is actually a fact
        if fact is Fact:
            # declare a variable for keeping track if the equal statement is found
            found = False
            # loop through all the available facts and check if the statement is equal to the fact attributes statement
            for i in range(len(self.facts)):
                if fact.statement == self.facts[i].statement:
                    fact = self.facts[i]
                    found = True
                    # found so we break out of the loop
                    break
            # check if the equal statement is not found, simply return None (null)
            if not found:
                return None
            # Finally, check if the length == 0, if it is we have to remove the fact from the facts list
            if len(fact.supported_by) == 0:
                self.facts.remove(fact)

        # Third, we have to check if the given parameter fact is actually of type Rule
        if fact is Rule:
            # if it is a rule, check if the len of the supported_by is 0 and if the rule is in the rule list already
            if len(fact.supported_by) == 0 and fact in self.rules:
                # if this is the case, remove the rule from the rules list
                self.rules.remove(fact)

        # Now loop through the supports_facts list in order to check if we have to remove and also retract the fact
        # To do so we call the following function
        fact_supports_loop_retract(fact.supports_facts, fact, self)
        # Now loop through the supports_rules list in order to check if we have to remove and also retract the rule
        # To do so we call the following function
        fact_supports_loop_retract(fact.supports_rules, fact, self)


def fact_supports_loop_retract(fact_supports_list, fact, self):

    for fact_or_rule in fact_supports_list:
        len_of_supported_by = len(fact_or_rule.supported_by)
        instances = 0
        # this is a counter which will be used to keep track of how many facts or rules are part of the supported by
        # list elements, if they are we remove them and we increment the counter
        for supported_by in fact_or_rule.supported_by:
            if fact in supported_by:
                fact_or_rule.supported_by.remove(supported_by)
                instances += 1
        # final step for each fact or rule is to check wheter our conter is equal to the length of the suppported by
        # list, this will mean that all the facts or rules are supported and we can retract the specific fact or rule
        # by calling the retract function
        if len_of_supported_by == instances:
            # if all facts or rules are supported by
            self.kb_retract(fact_or_rule)


class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
               [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here
        '''
        However, a rule might have multiple statements on its left-hand side (LHS), and we don't want to iterate each of
        these statements every time we add a new fact to the KB. Instead, we'll employ a cool trick. 
        Whenever we add a new rule, we'll only check the first element of the LHS of that rule against the facts in our
        KB. (If we add a new fact, we'll reverse this - we'll examine each rule in our KB and check the first element
        of its LHS against this new fact.) If there's a match with this first element, we'll add a new rule paired 
        with bindings for that match.
        '''
        # The first step is to use the match function as instructed in order to check if the
        # left-hand side (LHS) first element matches the statement of the fact.
        bindings = match(rule.lhs[0], fact.statement)
        # if we got no results, simply return None
        if not bindings:
            return None

        # The second step is to check whether we have one or multiple rules or facts in the LHS
        # IF we have multiple statements in the LHS of the rule:
        if len(rule.lhs) > 1:
            lhs_list = []
            rule_list = []
            for i in range(1, len(rule.lhs)):
                lhs_list.append(instantiate(rule.lhs[i], bindings))
            rule_list.append(lhs_list)
            rule_list.append(instantiate(rule.rhs, bindings))
            new_rule = Rule(rule_list, [[rule, fact]])
            rule.supports_rules.append(new_rule)
            fact.supports_rules.append(new_rule)
            kb.kb_add(new_rule)
        # only one LHS
        else:
            new_fact = Fact(instantiate(rule.rhs, bindings), [[rule, fact]])
            rule.supports_facts.append(new_fact)
            fact.supports_facts.append(new_fact)
            kb.kb_add(new_fact)
